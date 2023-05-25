import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from sklearn import metrics
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from transformers import CamembertForSequenceClassification, CamembertTokenizer, AdamW
import seaborn as sns
import matplotlib.pyplot as plt

# Chargement du jeu de données
cols = ['rate', 'review_text']
dataset = pd.read_csv("/Users/camille/repo/Hetic/projet_gouv/scraping/data_nlp/google_reviews_RGPD.csv", usecols=cols)
dataset['sentiment'] = dataset['rate'].apply(lambda x: 1 if x >= 2.5 else 0)
dataset.dropna(subset=['review_text'], inplace=True)
print(dataset.head())

# Division du jeu de données en train, eval, test
train_data, remaining_data = train_test_split(dataset, test_size=0.2, random_state=200)
eval_data, test_data = train_test_split(remaining_data, test_size=0.5, random_state=200)

print("Train Data Size:", len(train_data))
print("Eval Data Size:", len(eval_data))
print("Test Data Size:", len(test_data))

# On charge l'objet "tokenizer" de CamemBERT qui va servir à encoder
TOKENIZER = CamembertTokenizer.from_pretrained("camembert-base")
MAX_LENGTH = 128

# La fonction batch_encode_plus encode un batch de données
def batch_encode_plus(data):
    encoded_batch = TOKENIZER.batch_encode_plus(
        data,
        add_special_tokens=True,
        max_length=MAX_LENGTH,
        padding=True,
        truncation=True,
        return_attention_mask=True,
        return_tensors='pt')
    return encoded_batch

# Encoding des données d'entraînement
train_reviews = train_data['review_text'].values.tolist()
train_sentiments = train_data['sentiment'].values.tolist()
encoded_train_batch = batch_encode_plus(train_reviews)
train_dataset = TensorDataset(
    encoded_train_batch['input_ids'],
    encoded_train_batch['attention_mask'],
    torch.tensor(train_sentiments)
)

# Encoding des données d'évaluation
eval_reviews = eval_data['review_text'].values.tolist()
eval_sentiments = eval_data['sentiment'].values.tolist()
encoded_eval_batch = batch_encode_plus(eval_reviews)
eval_dataset = TensorDataset(
    encoded_eval_batch['input_ids'],
    encoded_eval_batch['attention_mask'],
    torch.tensor(eval_sentiments)
)

# Encoding des données de test
test_reviews = test_data['review_text'].values.tolist()
test_sentiments = test_data['sentiment'].values.tolist()
encoded_test_batch = batch_encode_plus(test_reviews)
test_dataset = TensorDataset(
    encoded_test_batch['input_ids'],
    encoded_test_batch['attention_mask'],
    torch.tensor(test_sentiments)
)

batch_size = 64

# On crée les DataLoaders d'entraînement, d'évaluation et de test
train_dataloader = DataLoader(
    train_dataset,
    sampler=RandomSampler(train_dataset),
    batch_size=batch_size
)

eval_dataloader = DataLoader(
    eval_dataset,
    sampler=SequentialSampler(eval_dataset),
    batch_size=batch_size
)

test_dataloader = DataLoader(
    test_dataset,
    sampler=SequentialSampler(test_dataset),
    batch_size=batch_size
)

# On va stocker nos tensors sur le GPU s'il est disponible, sinon sur le CPU
device = torch.device("cpu")
# Création du modèle
model = CamembertForSequenceClassification.from_pretrained("camembert-base")
model.to(device)

# Définition de l'optimizer et de la fonction de perte
optimizer = AdamW(model.parameters(), lr=1e-5)
loss_fn = torch.nn.CrossEntropyLoss()

# Pour enregistrer les statistiques à chaque époque
training_stats = []

# Boucle d'entraînement
epochs = 2  # Nombre d'époques
for epoch in range(epochs):
    print("")
    print(f'########## Epoch {epoch+1} / {epochs} ##########')
    print('Training...')

    # On initialise la loss pour cette époque
    total_train_loss = 0

    # On met le modèle en mode 'training'
    model.train()

    # Pour chaque batch
    for step, batch in enumerate(train_dataloader):

        # On fait un print chaque 40 batchs
        if step % 40 == 0 and not step == 0:
            print(f'Batch {step} of {len(train_dataloader)}.')

        # On récupère les données du batch
        input_ids = batch[0].to(device)
        attention_mask = batch[1].to(device)
        sentiment = batch[2].to(device)

        # On met le gradient à 0
        model.zero_grad()

        # On passe les données au modèle et on récupère les prédictions
        outputs = model(input_ids=input_ids,
                        attention_mask=attention_mask,
                        labels=sentiment)
        logits = outputs.logits

        # Calcul de la loss
        loss = loss_fn(logits.view(-1, model.config.num_labels), sentiment.view(-1))

        # On incrémente la loss totale
        total_train_loss += loss.item()

        # Rétropropagation
        loss.backward()

        # Mise à jour des paramètres
        optimizer.step()

    # Calcul de la loss moyenne sur toute l'époque
    avg_train_loss = total_train_loss / len(train_dataloader)

    print("")
    print("  Average training loss: {0:.2f}".format(avg_train_loss))

    # Enregistrement des statistiques de l'époque
    training_stats.append(
        {
            'epoch': epoch + 1,
            'Training Loss': avg_train_loss,
        }
    )

print("Training complete!")

# Évaluation du modèle sur les données d'évaluation
print("")
print("Running evaluation...")

# Mettre le modèle en mode d'évaluation
model.eval()

# Variables pour stocker les prédictions et les vraies étiquettes de l'évaluation
eval_predictions = []
eval_true_labels = []

# Pour chaque batch de données d'évaluation
for batch in eval_dataloader:
    # On récupère les données du batch
    input_ids = batch[0].to(device)
    attention_mask = batch[1].to(device)
    sentiment = batch[2].to(device)

    # Désactiver le calcul des gradients pendant l'évaluation
    with torch.no_grad():
        # On passe les données au modèle et on récupère les prédictions
        outputs = model(input_ids=input_ids,
                        attention_mask=attention_mask)
        logits = outputs.logits

    # Convertir les logits en prédictions
    pred = torch.argmax(logits, dim=1).flatten()

    # Ajouter les prédictions et les vraies étiquettes aux listes correspondantes
    eval_predictions.extend(pred)
    eval_true_labels.extend(sentiment)

# Convertir les listes en tenseurs
# Convert the tensors to CPU before converting to numpy arrays
eval_predictions = torch.tensor(eval_predictions).cpu().numpy()
eval_true_labels = torch.tensor(eval_true_labels).cpu().numpy()



# Calcul des métriques d'évaluation
eval_accuracy = metrics.accuracy_score(eval_true_labels, eval_predictions)
eval_precision = metrics.precision_score(eval_true_labels, eval_predictions)
eval_recall = metrics.recall_score(eval_true_labels, eval_predictions)
eval_f1_score = metrics.f1_score(eval_true_labels, eval_predictions)


# Affichage des métriques
print(f"Eval Accuracy: {eval_accuracy:.4f}")
print(f"Eval Precision: {eval_precision:.4f}")
print(f"Eval Recall: {eval_recall:.4f}")
print(f"Eval F1 Score: {eval_f1_score:.4f}")

# Matrice de confusion pour les données d'évaluation
"""eval_cm = metrics.confusion_matrix(eval_true_labels, eval_predictions)
plt.figure(figsize=(6, 6))
sns.heatmap(eval_cm, annot=True, fmt=".0f", linewidths=0.5, square=True, cmap="Blues")
plt.ylabel("True Label")
plt.xlabel("Predicted Label")
plt.title("Evaluation Confusion Matrix")
plt.show()"""

# Évaluation du modèle sur les données de test
print("")
print("Running test...")

# Variables pour stocker les prédictions et les vraies étiquettes des tests
test_predictions = []
test_true_labels = []

# Mettre le modèle en mode d'évaluation
model.eval()

# Pour chaque batch de données de test
for batch in test_dataloader:
    # On récupère les données du batch
    input_ids = batch[0].to(device)
    attention_mask = batch[1].to(device)
    sentiment = batch[2].to(device)

    # Désactiver le calcul des gradients pendant l'évaluation
    with torch.no_grad():
        # On passe les données au modèle et on récupère les prédictions
        outputs = model(input_ids=input_ids,
                        attention_mask=attention_mask)
        logits = outputs.logits

    # Convertir les logits en prédictions
    pred = torch.argmax(logits, dim=1).flatten()

    # Ajouter les prédictions et les vraies étiquettes aux listes correspondantes
    test_predictions.extend(pred)
    test_true_labels.extend(sentiment)

# Convertir les listes en tenseurs
test_predictions = torch.stack(test_predictions)
test_true_labels = torch.stack(test_true_labels)

# Calcul des métriques d'évaluation
test_accuracy = metrics.accuracy_score(test_true_labels, test_predictions)
test_precision = metrics.precision_score(test_true_labels, test_predictions)
test_recall = metrics.recall_score(test_true_labels, test_predictions)
test_f1_score = metrics.f1_score(test_true_labels, test_predictions)

# Affichage des métriques
print(f"Test Accuracy: {test_accuracy:.4f}")
print(f"Test Precision: {test_precision:.4f}")
print(f"Test Recall: {test_recall:.4f}")
print(f"Test F1 Score: {test_f1_score:.4f}")

# Matrice de confusion pour les données de test
test_cm = metrics.confusion_matrix(test_true_labels, test_predictions)
plt.figure(figsize=(6, 6))
sns.heatmap(test_cm, annot=True, fmt=".0f", linewidths=0.5, square=True, cmap="Blues")
plt.ylabel("True Label")
plt.xlabel("Predicted Label")
plt.title("Test Confusion Matrix")
plt.show()

# Enregistrement du modèle
torch.save(model.state_dict(), "./sentiments.pt")
print("Model saved!")


# Convert the test predictions and true labels to lists
test_predictions_list = test_predictions.tolist()
test_true_labels_list = test_true_labels.tolist()

# Create a dictionary to store the results
results = {"predictions": test_predictions_list, "true_labels": test_true_labels_list}

# Save the results to a file
pd.DataFrame(results).to_csv("sentiment_results.csv", index=False)
print("Results saved!")

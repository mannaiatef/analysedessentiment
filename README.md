# Analyse de Sentiment

Une application d'analyse de sentiment et de résumé de texte utilisant les modèles de Hugging Face.

## Fonctionnalités

- **Analyse de sentiment** : Détecte si un texte est positif, négatif ou neutre
- **Résumé de texte** : Génère un résumé concis d'un texte plus long
- **Interface graphique** : Interface utilisateur simple et intuitive
- **Statistiques** : Suivi du nombre d'analyses par catégorie de sentiment

## Prérequis

- Python 3.6 ou supérieur
- Connexion Internet (pour les appels API)
- Un token d'API Hugging Face

## Installation

1. Clonez ce dépôt :
```
git clone https://github.com/mannaiatef/analysedessentiment.git
cd analysedesentiment
```

2. Installez les dépendances :
```
pip install requests matplotlib tkinter
```

3. Configurez votre token API :
   - Ouvrez le fichier `temp.py`
   - Remplacez `YOUR_HUGGING_FACE_TOKEN` par votre token d'API Hugging Face

## Utilisation

1. Lancez l'application :
```
python temp.py
```

2. Entrez le texte à analyser dans la zone de texte
3. Choisissez entre l'analyse de sentiment ou le résumé de texte
4. Cliquez sur "Exécuter" pour obtenir les résultats

## Modèles utilisés

- **Analyse de sentiment** : cardiffnlp/twitter-roberta-base-sentiment-latest
- **Résumé de texte** : facebook/bart-large-cnn

## Sécurité

⚠️ Ne partagez jamais votre token d'API dans des dépôts publics. Utilisez des variables d'environnement ou des fichiers de configuration exclus du contrôle de version pour stocker vos informations sensibles.
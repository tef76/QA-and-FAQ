# QA-and-FAQ
L'objectif du projet était de faire marcher un pipeline de Question Answering.
Pour cela j'ai dû apprendre à utiliser la librairie Haystack.

## Test de la Pipeline

Dans un premier temps j'ai téléchargé deux modèles sur huging face pour les tester. Le premier est un retriever, il a donc pour but de chercher les documents qui sont le plus relevant par rapport à la question. Le deuxième est un reader, son but va être, au sein des documents de trouvé la réponse à la question.

Voir Test_Pipeline_QA.ipynb pour le code de test des modèles. 

### Résultat Retriever:

![image](https://user-images.githubusercontent.com/40719576/229810127-d9513660-69d6-4f71-9a7c-ffd8bd95fd92.png)

### Résultat Reader:

![image](https://user-images.githubusercontent.com/40719576/229810187-9ff4304a-2017-46f8-afe2-262edf5fbf2b.png)

### QA 

Dans un deuxième temps l'objectif était de tester le pipeline dans un cas réel, pour cela j'ai choisi la faq de carrefour. Pour cela j'ai utilisé Streamlit pour avoir une interface simple de la pipeline.
On peut voir que le système de QA n'est pas très approprié pour de la FAQ, haystack possède un pipeline dédié à la FAQ que j'ai donc utilisé dans une dernière partie du projet.

![image](https://user-images.githubusercontent.com/40719576/229843739-9b893381-c25e-495e-9186-59c4fe013749.png)


### FAQ

![image](https://user-images.githubusercontent.com/40719576/229842804-7b6557a7-51f6-4ba2-a1b6-1bba84b2b254.png)

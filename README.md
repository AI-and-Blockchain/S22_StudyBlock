# S22_StudyBlock
# Project Description 
To create a platform that allows cancer researchers and patients to be matched to clinical trials and research studies according to their needs. The project will use AI to provide matches for researchers and patients. The project will require blockchain in order for patients and/or researchers to be able to contact the point of contact of the clinical trials or research studies where there can also be a safe medium of private data exchange if need be.

# Motivation
Improve patient and researcher access to clinical trials and research studies which in turn benefits the trials and studies as well.

# Final Goal
To allow patients and researchers to be matched with clinical trials that match their needs and to allow researchers to negotiate for clinical research data on the blockchain.


# User Stories
As a breast cancer patient, I want to be able to further look into the effects and results of a clinical trial to find the one that best suits my needs. 

As a researcher, I want to find clinical trial data related to my current study to help support my current research.

# StudyBlock User Work Flow
```mermaid
graph TB;
    A[Research Owner] -- Advertises Clinical Trial <br> to BlockChain --> D[Clinical Trial <br> Description on chain]
    A -- Stores data/private <br> information off chain --> E[Clinical Trial Data]
    B[Researcher] -- Uses NLP Algorithm <br> to search for <br> relevant studies --> F[List of matching <br> clinical trials]
    C[Patient] -- Uses NLP Algorithm <br> to search for <br> relevant studies --> F
    F -- Researcher/Patient <br> finds a matching study --> D
    D -- Patient reaches out <br> to research owner --> G[Research Owner and patient <br> line of communication, <br> so patient can potentially be added <br> to the clinical trial]
    D -- Researcher reaches <br> out to research owner, <br> research owner can chose <br> to then share off-chain <br> data with researcher --> E
```

# StudyBlock Architecture
```mermaid
graph LR;
A[NLP powered search feature] -- List of custom assets <br> that represent clinical <br> trial studies --->
B[Clinical Trial #1 <br> Clinical Trial #2 <br> Clinical Trial #3 <br> etc.]
B -- User calls smart contract --- C[ ]:::empty
C --> D[Smart contract #1: <br> Potential patient for study] 
C --> E[Smart Contract #2: <br> Researcher looking for information]
classDef empty width:0px,height:0px;

```

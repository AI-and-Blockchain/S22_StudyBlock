# S22_StudyBlock
Project Description: 
To create a platform that allows cancer researchers and patients to be matched
to clinical trials and research studies according to their needs to help
further improve patient and researcher access to clinical trials and research
studies which in turn benefits the trials and studies as well. The project will
use AI to provide matches for researchers and patients. The project will require
blockchain in order for patients and/or researchers to be able to contact the 
point of contact of the clinical trials or research studies where there can also 
be a safe medium of private data exchange if need be. 


# StudyBlock User Work Flow
```mermaid
graph TB;
    A[Research Owner] - Advertises Clinical Trial to BlockChain -> D[Clinical Trial Description on chain]
    A - Stores data/private information off chain -> E[Clinical Trial Data]
    B[Researcher] - Uses NLP Algorithm to search for relevant studies -> F[List of matching clinical trials]
    C[Patient] - Uses NLP Algorithm to search for relevant studies -> F
    F - Researcher/Patient finds a matching study -> D
    D - Patient reaches out to research owner -> G[Research Owner and patient line of communication, so patient can potentially be added to the clinical trial]
    D - Researcher reaches out to research owner, research owner can chose to then share off chain data with researcher -> E
```


METADATA :

Hindi_SoundFile_Verification_data_sample.csv :

Contains the text prompts converted , the text feedback , the audio name and the audio feedback .

user-id -> Anonymous user-id of the speaker
text -> The text spoken by the user
audioFileName -> Name of the audio-file as present in the 'Sound Files' folder
audioLength -> Length of the audio recorded
commentMsg -> Comment on the text prompt by the user contributing the voice
language -> Language of the text prompt

Comment on the feedback of the audio : (Number of Comments)
AIF -> Audio is Fine
TAADNM -> Text and audio do not match
ICA -> Incomplete audio
SVIU -> Speaker's voice is unclear
BIN -> Background is noisy
IA -> Inaudible
VIROA -> Voice is Robotic /Artificial

User_demographics.csv :

Contains user data linked to Hindi_SoundFile_Verification_data_sample.csv via user-id :

user-id -> Anonymous user-id of the speaker
Gender -> user gender
Age -> user age
prefLanguage -> Language(s) selected by the user to contribute in
fluentLanguage -> Language(s) user deems to have fluency in. This is a subset of prefLanguage

Sound Files :

Contains audio files of the tasks contributed with the same nomenclature as defined in Hindi_SoundFile_Verification_data_sample.csv




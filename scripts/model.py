from deepface import DeepFace

def predictEmotionFace(img):
    result = DeepFace.analyze(img_path = img, actions = ['emotion'])
    emotions = result[0]['emotion']

    top_emotion = max(emotions, key=emotions.get)
    return top_emotion
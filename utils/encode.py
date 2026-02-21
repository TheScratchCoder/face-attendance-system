import face_recognition
import os
import pickle

KNOWN_FACES_DIR = "known_faces"
ENCODINGS_PATH = "encodings/encodings.pkl"


def encode_faces():
    """
    Scan all images in known_faces/, encode each face,
    and save encodings + names to a pickle file.
    Filename format: Name_RollNo.jpg
    """
    known_encodings = []
    known_names = []

    supported = (".jpg", ".jpeg", ".png")

    for filename in os.listdir(KNOWN_FACES_DIR):
        if not filename.lower().endswith(supported):
            continue

        filepath = os.path.join(KNOWN_FACES_DIR, filename)
        image = face_recognition.load_image_file(filepath)
        encodings = face_recognition.face_encodings(image)

        if encodings:
            # Use first detected face
            known_encodings.append(encodings[0])
            # Extract name (everything before first underscore or last dot)
            name = os.path.splitext(filename)[0]  # remove extension
            name = name.split("_")[0]              # take name part before roll
            known_names.append(name)
            print(f"[✓] Encoded: {name} from {filename}")
        else:
            print(f"[✗] No face found in: {filename}")

    os.makedirs("encodings", exist_ok=True)
    with open(ENCODINGS_PATH, "wb") as f:
        pickle.dump((known_encodings, known_names), f)

    print(f"\n✅ Total encoded: {len(known_encodings)} faces")
    return known_encodings, known_names


if __name__ == "__main__":
    encode_faces()

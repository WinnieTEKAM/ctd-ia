import requests

API_URL = "http://localhost:3000/api/posts"

def send_post(titre, resume, content, content_anonymise, topic, hashtags, language, completude):
    body = {
        "titre":             titre,
        "resume":            resume,
        "content":           content,
        "content_anonymise": content_anonymise,
        "topic":             topic,
        "hashtags":          hashtags,
        "language":          language,
        "status":            "brouillon",
        "completude":        completude
    }

    try:
        response = requests.post(API_URL, json=body)

        if response.status_code == 201:
            print("Post envoye avec succes !")
            print("ID du post :", response.json().get("id"))
            return response.json()
        else:
            print("Erreur :", response.status_code, response.json())
            return None

    except Exception as e:
        print("Erreur serveur :", e)
        return None


if __name__ == "__main__":
    send_post(
        titre            = "Patient 72 ans - implantation pacemaker (Brady)",
        resume           = "Indication : BAV 3eme degre. Procedure sans complication.",
        content          = "Patient de 72 ans. BAV 3eme degre. Implantation pacemaker LBBAP. #pacemaker #BAV #Brady",
        content_anonymise= "[PATIENT] de 72 ans. BAV 3eme degre. Implantation pacemaker LBBAP. #pacemaker #BAV #Brady",
        topic            = "Brady",
        hashtags         = "#pacemaker #BAV #Brady #LBBAP",
        language         = "fr",
        completude       = True
    )

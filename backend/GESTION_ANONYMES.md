# Gestion des Utilisateurs Anonymes - Documentation

## Modifications Apportées

### 1. Vue `upload_and_score` (views.py)

La vue a été modifiée pour supporter **à la fois** les utilisateurs authentifiés et anonymes :

```python
@api_view(['POST'])
@permission_classes([AllowAny])  # ✅ Permet l'accès sans authentification
@transaction.atomic
def upload_and_score(request):
```

#### Logique de gestion des utilisateurs

```python
# Associer l'utilisateur seulement s'il est authentifié
if request.user and request.user.is_authenticated:
    candidate = serializer.save(user=request.user)
    logger.info(f"Candidat {candidate.id} créé par utilisateur authentifié")
else:
    candidate = serializer.save(user=None)
    logger.info(f"Candidat {candidate.id} créé en mode anonyme")
```

### 2. Modèle Candidate (models.py)

Le champ `user` est déjà configuré pour accepter les valeurs NULL :

```python
class Candidate(models.Model):
    # ... autres champs ...
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
```

✅ **Aucune migration nécessaire** - le modèle supportait déjà les utilisateurs NULL.

### 3. Logging Amélioré

Ajout de logs pour suivre les créations de candidats :

- **Authentifié** : Log l'ID de l'utilisateur
- **Anonyme** : Log l'email du candidat
- **Pas de CV** : Warning si aucun CV n'est trouvé après création
- **Erreurs** : Log détaillé avec stack trace (`exc_info=True`)

## Comportement

### Cas d'Usage 1 : Utilisateur Authentifié

**Requête :**

```http
POST /api/cvs/upload/
Authorization: Bearer <token>
Content-Type: multipart/form-data

{
  "name": "Jean Dupont",
  "email": "jean@example.com",
  "phone": "+33612345678",
  "job": "uuid-job-id",
  "file": <fichier-cv>
}
```

**Résultat :**

- Candidat créé avec `user=request.user`
- Association traçable dans la base
- Log : "Candidat créé par utilisateur authentifié {user_id}"

### Cas d'Usage 2 : Utilisateur Anonyme

**Requête :**

```http
POST /api/cvs/upload/
Content-Type: multipart/form-data

{
  "name": "Marie Martin",
  "email": "marie@example.com",
  "phone": "+33687654321",
  "job": "uuid-job-id",
  "file": <fichier-cv>
}
```

**Résultat :**

- Candidat créé avec `user=None`
- Candidature publique sans lien utilisateur
- Log : "Candidat créé en mode anonyme: {email}"

## Sécurité et Recommandations

### ✅ Avantages

1. **Flexibilité** : Support des deux modes (authentifié/anonyme)
2. **Traçabilité** : Les utilisateurs authentifiés restent traçables
3. **Accessibilité** : Pas de barrière à l'entrée pour les candidatures

### ⚠️ Points d'Attention

1. **Spam** : Les candidatures anonymes peuvent être sujettes au spam

   - **Recommandation** : Ajouter un rate limiting (django-ratelimit)
   - **Recommandation** : Implémenter un CAPTCHA (reCAPTCHA)

2. **Données personnelles (RGPD)** :

   - Les emails et téléphones anonymes doivent être protégés
   - Implémenter une politique de rétention des données
   - Permettre la suppression sur demande

3. **Validation email** :
   - Considérer l'envoi d'un email de confirmation
   - Éviter les emails jetables/temporaires

### 🔧 Améliorations Possibles

#### 1. Rate Limiting (Anti-Spam)

```python
from django_ratelimit.decorators import ratelimit

@api_view(['POST'])
@permission_classes([AllowAny])
@ratelimit(key='ip', rate='5/h', method='POST')  # 5 candidatures/heure par IP
@transaction.atomic
def upload_and_score(request):
    # ... code existant
```

#### 2. Validation Email Avancée

```python
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def validate_professional_email(email):
    """Rejette les emails jetables connus"""
    disposable_domains = ['tempmail.com', '10minutemail.com', 'guerrillamail.com']
    domain = email.split('@')[1]
    if domain in disposable_domains:
        raise ValidationError("Les emails temporaires ne sont pas acceptés")
```

#### 3. Notification Email de Confirmation

```python
from django.core.mail import send_mail

def send_application_confirmation(candidate):
    """Envoie un email de confirmation au candidat"""
    send_mail(
        subject='Candidature reçue',
        message=f'Bonjour {candidate.name},\n\nVotre candidature a été reçue avec succès.',
        from_email='noreply@ats.com',
        recipient_list=[candidate.email],
        fail_silently=True
    )
```

## Tests

### Test 1 : Candidature Anonyme

```bash
curl -X POST http://127.0.0.1:8000/api/cvs/upload/ \
  -F "name=Test User" \
  -F "email=test@example.com" \
  -F "phone=0612345678" \
  -F "job=<job-uuid>" \
  -F "file=@cv.pdf"
```

### Test 2 : Candidature Authentifiée

```bash
curl -X POST http://127.0.0.1:8000/api/cvs/upload/ \
  -H "Authorization: Bearer <token>" \
  -F "name=Auth User" \
  -F "email=auth@example.com" \
  -F "phone=0687654321" \
  -F "job=<job-uuid>" \
  -F "file=@cv.pdf"
```

## Monitoring

### Logs à Surveiller

```python
# Info : création réussie
logger.info(f"Candidat {candidate.id} créé par utilisateur authentifié {user.id}")
logger.info(f"Candidat {candidate.id} créé en mode anonyme: {email}")

# Warning : pas de CV uploadé
logger.warning(f"Aucun CV trouvé pour candidat {candidate.id}")

# Error : échec du scoring
logger.error(f"Erreur lors du calcul de score pour candidat {candidate.id}: {error}")
```

### Métriques Recommandées

1. **Ratio authentifié/anonyme** : Surveiller la proportion de chaque type
2. **Taux de conversion** : Candidatures avec CV vs sans CV
3. **Erreurs de scoring** : Identifier les problèmes de traitement
4. **Temps de traitement** : Optimiser les performances

## Migration Base de Données

✅ **Aucune migration nécessaire** car le champ `user` du modèle `Candidate` était déjà configuré avec `null=True, blank=True`.

Si vous partez d'une base existante où le champ était `NOT NULL`, créez une migration :

```bash
python manage.py makemigrations
python manage.py migrate
```

## Questions Fréquentes

### Q: Les candidatures anonymes ont-elles un score ?

**R:** Oui, le scoring fonctionne de la même manière pour les deux types d'utilisateurs.

### Q: Peut-on retrouver les candidatures d'un utilisateur anonyme ?

**R:** Seulement par email ou téléphone via des recherches en base.

### Q: Comment éviter les doublons ?

**R:** Implémenter une validation côté serializer pour vérifier l'unicité email+job.

### Q: Les anonymes peuvent-ils modifier leur candidature ?

**R:** Non, sans authentification ils ne peuvent pas accéder à leurs données. Considérer l'ajout d'un lien magique par email.

## Support et Maintenance

Pour toute question ou problème :

1. Consulter les logs Django : `tail -f logs/django.log`
2. Vérifier le monitoring : dashboard APM
3. Tester manuellement via curl ou Postman

---

**Date de création** : 13 octobre 2025  
**Dernière mise à jour** : 13 octobre 2025

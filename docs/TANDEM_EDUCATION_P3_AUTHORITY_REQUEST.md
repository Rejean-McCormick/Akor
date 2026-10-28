# Tandem Éducation P3 — Akor (demande non fiable)

- `akor.tandem-authority-request/1.0` est une **demande**, jamais une autorisation.
- Le producteur `src/akor/tandem_authority_request.py` valide les champs P2 en liste blanche, les UUID, les empreintes, la non-duplication des tâches et le fait que TOUS les indicateurs d'autorité sont `false`.
- La demande contient le SHA-256 des octets bruts de l'intention P2 (pas une signature). Elle ne transporte ni personne, ni rôle scolaire reconnu, ni indice caché.
- Akor n'a pas le droit de créer un actor Orgo, une session, un token d'enseignant ou une WorldRelease.
- Une demande P3 valide ne constitue pas un droit de lancer une mission : son statut est `AWAITING_SERVER_VERIFICATION`.
- Le service destinataire doit vérifier l'identité Orgo lui-même, consulter les données courantes du World et de l'approbation enseignante, et produire la décision dans une transaction idempotente (pas implémenté en P3).
- Aucun HTTP, aucune base, aucun VPS ni aucun enfant n'est impliqué dans cet ajout.

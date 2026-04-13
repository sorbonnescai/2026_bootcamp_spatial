"""
Matching groupes → projets via l'algorithme Hospital-Resident (Gale-Shapley).
Contrainte : 1 projet pour exactement 2 groupes (capacité = 2).
"""

def gale_shapley_hospital_resident(group_prefs: dict, project_capacity: dict) -> dict:
    """
    group_prefs      : {groupe_id: [proj_1, proj_2, ...]}  (du plus au moins préféré)
    project_capacity : {projet_id: capacité}               (ici 2 pour tous)
    
    Retourne : {groupe_id: projet_id}
    """
    # File des groupes non encore matchés
    free_groups = list(group_prefs.keys())
    
    # Pointeur sur la prochaine préférence à proposer pour chaque groupe
    next_proposal = {g: 0 for g in group_prefs}
    
    # Groupes actuellement acceptés par chaque projet
    project_accepted = {p: [] for p in project_capacity}
    
    while free_groups:
        group = free_groups.pop(0)
        prefs = group_prefs[group]
        
        # Plus de projets à proposer → groupe non matchable
        if next_proposal[group] >= len(prefs):
            print(f"⚠️  Groupe {group} n'a pu être matché (préférences épuisées)")
            continue
        
        # Propose au prochain projet sur sa liste
        project = prefs[next_proposal[group]]
        next_proposal[group] += 1
        accepted = project_accepted[project]
        capacity = project_capacity[project]
        
        if len(accepted) < capacity:
            # Place disponible → accepté directement
            accepted.append(group)
        else:
            # Projet plein → on cherche le groupe le moins bien classé parmi les acceptés
            # Les projets n'ont pas de préférences ici → on utilise l'ordre d'arrivée
            # (variante : tu peux ajouter des préférences projets si besoin)
            worst = accepted[-1]  # dernier accepté = moins prioritaire
            accepted.remove(worst)
            accepted.append(group)
            free_groups.append(worst)  # worst repart chercher un autre projet
    
    # Construit le mapping final groupe → projet
    result = {}
    for project, groups in project_accepted.items():
        for g in groups:
            result[g] = project
    return result


def run_matching(students: list, group_size_hint: int = 2):
    """
    Exemple d'utilisation avec constitution automatique des groupes.
    
    students        : liste des étudiants
    group_size_hint : taille préférée des groupes (2 ou 3)
    """
    import math

    n = len(students)
    
    # Constitution des groupes (groupes de 3 si nécessaire pour tout le monde)
    groups = []
    i = 0
    group_id = 1
    while i < n:
        remaining = n - i
        # Si le reste ne se divise pas bien par 2, on fait un groupe de 3
        if remaining % 2 == 1 and remaining >= 3:
            groups.append({
                "id": f"G{group_id}",
                "members": students[i:i+3]
            })
            i += 3
        else:
            groups.append({
                "id": f"G{group_id}",
                "members": students[i:i+2]
            })
            i += 2
        group_id += 1

    n_groups = len(groups)
    n_projects = math.ceil(n_groups / 2)  # 1 projet pour 2 groupes
    projects = [f"P{j+1}" for j in range(n_projects)]

    print(f"👥 {n} étudiants → {n_groups} groupes → {n_projects} projets")
    print(f"Groupes : {[g['id'] for g in groups]}")
    print(f"Projets : {projects}\n")

    return groups, projects


# ── Exemple concret ──────────────────────────────────────────────────────────

if __name__ == "__main__":

    # 1. Préférences des groupes (saisies par les étudiants)
    group_prefs = {
        1: ['P1', 'P4', 'P2', 'P3'],
        2: ['P1', 'P3', 'P2', 'P4'],
        3: ['P4', 'P2', 'P1', 'P3'],
        4: ['P2', 'P4', 'P3', 'P1'],
        5: ['P3', 'P1', 'P2', 'P4'],
        6: ['P2', 'P3', 'P4', 'P1'],
        7: ['P3', 'P4', 'P1', 'P2'],
        8: ['P3', 'P2', 'P1', 'P4']
    }

    print("📋 Préférences des groupes :")
    for gid, prefs in group_prefs.items():
        print(f"  Groupe {gid} : {prefs}")
    print()

    # 2. Capacité des projets (2 groupes par projet)
    group_ids = list(group_prefs.keys())
    projects = ['P1', 'P2', 'P3', 'P4']
    project_capacity = {p: 2 for p in projects}

    # 3. Lancement du matching
    result = gale_shapley_hospital_resident(group_prefs, project_capacity)

    # 4. Affichage des résultats
    print("\n✅ Résultat du matching :")
    from collections import defaultdict
    proj_to_groups = defaultdict(list)
    for group, project in result.items():
        proj_to_groups[project].append(group)

    for project in sorted(proj_to_groups):
        grps = proj_to_groups[project]
        print(f"  {project} ← {grps}")

    # Groupes non matchés
    unmatched = [g for g in group_ids if g not in result]
    if unmatched:
        print(f"\n⚠️  Groupes non matchés : {unmatched}")
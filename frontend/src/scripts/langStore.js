// frontend/src/scripts/langStore.js

// Dictionnaire de traduction statique
const translations = {
  en: {
    "search_placeholder": "Search Pokémon...",
    "my_team": "My Team",
    "show_stats": "Show statistics",
    "nature": "Nature",
    "held_item": "Held Item",
    "add_pokemon": "+ Add Pokémon",
    "pokedex": "Pokédex",
    "type": "Type",
    "abilities": "Abilities",
    "add_to_team": "Add to Team",
    "remove_from_team": "Remove",
    "added_to_team": "Added to Team!",
    "removed_from_team": "Removed from Team!",
    "team_full": "Team is full (Max 6)!",
    "empty_team_title": "Your team is empty!",
    "empty_team_desc": "Add your favorite Pokémon from the list below.",
    "team_limit": "Max 6 Pokémon per team.",
    "nature": "Nature",
    "held_item": "Held Item",
    "no_item": "No item",
    "remove": "Remove",
    "hidden": "Hidden",
    "team_default": "Team",
    "configure": "Configure",
    "select_ability": "-- Select Ability --",
    "select_move_1": "-- Select Move 1 --",
    "select_move_2": "-- Select Move 2 --",
    "select_move_3": "-- Select Move 3 --",
    "select_move_4": "-- Select Move 4 --",
    "ev_hint": "Max 32 points per stat.",
    "ev_stats": "EV Stats",
    "move": "Move",
    "stats": "Base Stats",
    "stat_hp": "HP",
    "stat_attack": "Attack",
    "stat_defense": "Defense",
    "stat_special-attack": "Sp. Atk",
    "stat_special-defense": "Sp. Def",
    "stat_speed": "Speed",
    "ev_hp": "HP",
    "ev_attack": "Atk",
    "ev_defense": "Def",
    "ev_special-attack": "SpA",
    "ev_special-defense": "SpD",
    "ev_speed": "Spe",
    "moves": "Moves",
    "level": "Level",
    "power": "Power",
    "accuracy": "Accuracy",
    "pp": "PP",
    "category": "Category",
    "close": "Close",
    "save": "Save",
    "search": "Search",
    "no_item": "No item",
    "remove": "Remove",
    "hidden": "Hidden",
    "team_default": "Team",
    "repartition": "Stat Repartition",
    "create_manage_teams": "Create and manage your dream teams! (Maximum 6 Pokémon per team)",
    "explore_all": "Explore all the",
    "pokemon_on": "Pokémon on Pokemon Champions!",
    "back_to_pokedex": "← Back to Pokédex",
    "add_to_team": "Add to team",
    "base_stats": "Base Stats",
    "type_defenses": "Type Defenses",
    "rename_team": "Rename team",
    "create_new_team": "Create new team",
    "export": "EXPORT",
    "weight": "Weight",
    "height": "Height",
    "weak_to": "Weak to",
    "resists": "Resists",
    "immune_to": "Immune to",
    "nature": "Nature",
    "item": "Item",
    "held_item": "Held Item",
    "abilities": "Ability",
    "ability": "Ability",
    "moves": "Moves (Max 4)",
    "no_item": "-- No Item --",
    "type_all": "All",
    "moves_champions": "Moves (Champions)",
    "all_types": "All types",
    "all_categories": "All categories",
    "az_order": "A-Z Order",
    "forms": "Forms",
    "stats_applied": "(Stats applied in Pokémon Champions)",
    "stat_hp": "HP",
    "stat_attack": "ATTACK",
    "stat_defense": "DEFENSE",
    "stat_special-attack": "SPECIAL ATTACK",
    "stat_special-defense": "SPECIAL DEFENSE",
    "stat_speed": "SPEED",
    "move_physical": "physical",
    "move_status": "status",
    "move_special": "special",
    "type_normal": "Normal",
    "type_fire": "Fire",
    "type_water": "Water",
    "type_electric": "Electric",
    "type_grass": "Grass",
    "type_ice": "Ice",
    "type_fighting": "Fighting",
    "type_poison": "Poison",
    "type_ground": "Ground",
    "type_flying": "Flying",
    "type_psychic": "Psychic",
    "type_bug": "Bug",
    "type_rock": "Rock",
    "type_ghost": "Ghost",
    "type_dragon": "Dragon",
    "type_dark": "Dark",
    "type_steel": "Steel",
    "type_fairy": "Fairy"
  },
  fr: {
    "search_placeholder": "Rechercher un Pokémon...",
    "my_team": "Mon Équipe",
    "empty_team_title": "Votre équipe est vide !",
    "empty_team_desc": "Ajoutez vos Pokémon préférés depuis la liste ci-dessous.",
    "show_stats": "Afficher les statistiques",
    "nature": "Nature",
    "held_item": "Objet Tenu",
    "add_pokemon": "+ Ajouter",
    "pokedex": "Pokédex",
    "type": "Type",
    "abilities": "Talents",
    "stats": "Statistiques de base",
    "stat_hp": "PV",
    "stat_attack": "Attaque",
    "stat_defense": "Défense",
    "stat_special-attack": "Atq. Spé",
    "stat_special-defense": "Déf. Spé",
    "stat_speed": "Vitesse",
    "ev_hp": "PV",
    "ev_attack": "Atq",
    "ev_defense": "Déf",
    "ev_special-attack": "Atq.S",
    "ev_special-defense": "Déf.S",
    "ev_speed": "Vit",
    "moves": "Attaques",
    "level": "Niveau",
    "power": "Puissance",
    "accuracy": "Précision",
    "pp": "PP",
    "category": "Catégorie",
    "close": "Fermer",
    "save": "Enregistrer",
    "search": "Rechercher",
    "no_item": "Aucun objet",
    "remove": "Retirer",
    "hidden": "Caché",
    "team_default": "Équipe",
    "configure": "Configurer",
    "select_ability": "-- Choisir un Talent --",
    "select_move_1": "-- Choisir l'Attaque 1 --",
    "select_move_2": "-- Choisir l'Attaque 2 --",
    "select_move_3": "-- Choisir l'Attaque 3 --",
    "select_move_4": "-- Choisir l'Attaque 4 --",
    "ev_hint": "Maximum 32 points par statistique.",
    "ev_stats": "Statistiques d'EV",
    "move": "Capacité",
    "repartition": "Répartition",
    "create_manage_teams": "Créez et gérez vos équipes de rêve ! (Maximum 6 Pokémon par équipe)",
    "explore_all": "Explorez les",
    "pokemon_on": "Pokémon présents sur Pokemon Champions !",
    "back_to_pokedex": "← Retour au Pokédex",
    "add_to_team": "Ajouter à l'équipe",
    "base_stats": "Statistiques de base",
    "type_defenses": "Faiblesses & Résistances",
    "rename_team": "Renommer l'équipe",
    "create_new_team": "Créer une équipe",
    "export": "EXPORTER",
    "weight": "Poids",
    "height": "Taille",
    "weak_to": "Faible face à",
    "resists": "Résiste à",
    "immune_to": "Immunisé à",
    "nature": "Nature",
    "item": "Objet",
    "held_item": "Objet tenu",
    "abilities": "Talent",
    "ability": "Talent",
    "moves": "Capacités (Max 4)",
    "no_item": "-- Aucun Objet --",
    "type_all": "Tous",
    "moves_champions": "Capacités (Champions)",
    "all_types": "Tous les types",
    "all_categories": "Toutes les catégories",
    "az_order": "Ordre A-Z",
    "forms": "Formes",
    "stats_applied": "(Statistiques appliquées dans Pokémon Champions)",
    "stat_hp": "PV",
    "stat_attack": "ATTAQUE",
    "stat_defense": "DÉFENSE",
    "stat_special-attack": "ATTAQUE SPÉCIALE",
    "stat_special-defense": "DÉFENSE SPÉCIALE",
    "stat_speed": "VITESSE",
    "move_physical": "physique",
    "move_status": "statut",
    "move_special": "spécial",
    "type_normal": "Normal",
    "type_fire": "Feu",
    "type_water": "Eau",
    "type_electric": "Électrik",
    "type_grass": "Plante",
    "type_ice": "Glace",
    "type_fighting": "Combat",
    "type_poison": "Poison",
    "type_ground": "Sol",
    "type_flying": "Vol",
    "type_psychic": "Psy",
    "type_bug": "Insecte",
    "type_rock": "Roche",
    "type_ghost": "Spectre",
    "type_dragon": "Dragon",
    "type_dark": "Ténèbres",
    "type_steel": "Acier",
    "type_fairy": "Fée"
  }
};

export function getLang() {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('poke_lang') || 'en';
  }
  return 'en';
}

export function setLang(lang) {
  if (typeof window !== 'undefined') {
    localStorage.setItem('poke_lang', lang);
    window.dispatchEvent(new CustomEvent('lang-changed', { detail: lang }));
    translateDOM();
  }
}

export function t(key) {
  const lang = getLang();
  return translations[lang]?.[key] || translations['en'][key] || key;
}

export function translateDOM() {
  if (typeof document !== 'undefined') {
    const lang = getLang();

    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (key) {
        if (el.tagName === 'INPUT' && el.type === 'text') {
            el.placeholder = t(key);
        } else {
            // Keep child elements if any, otherwise set textContent
            if (el.children.length === 0) {
               el.textContent = t(key);
            }
        }
      }
    });

    document.querySelectorAll('[data-i18n-title]').forEach(el => {
      const key = el.getAttribute('data-i18n-title');
      if (key) {
        el.setAttribute('title', t(key));
      }
    });

    document.querySelectorAll('[data-name-en]').forEach(el => {
      const lang = getLang();
      const text = el.getAttribute(`data-name-${lang}`);
      if (text) {
        el.innerHTML = text.replace(/\n/g, "<br>");
      }
    });
  }
}

// Initial translation on load
if (typeof document !== 'undefined') {
  document.addEventListener('DOMContentLoaded', () => {
    translateDOM();
  });
}

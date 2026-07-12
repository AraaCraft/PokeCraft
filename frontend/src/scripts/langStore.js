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
    "stats": "Base Stats",
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
    "repartition": "Stat Repartition"
  },
  fr: {
    "search_placeholder": "Rechercher un Pokémon...",
    "my_team": "Mon Équipe",
    "show_stats": "Afficher les statistiques",
    "nature": "Nature",
    "held_item": "Objet Tenu",
    "add_pokemon": "+ Ajouter",
    "pokedex": "Pokédex",
    "type": "Type",
    "abilities": "Talents",
    "stats": "Statistiques de base",
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
    "repartition": "Répartition"
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
  }
}

// Initial translation on load
if (typeof document !== 'undefined') {
  document.addEventListener('DOMContentLoaded', () => {
    translateDOM();
  });
}

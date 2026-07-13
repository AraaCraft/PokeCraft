// Cookie management for Pokémon Team
const TEAM_COOKIE_NAME = 'pokecraft_team';
const MAX_TEAM_SIZE = 6;

// Helper to get cookie value by name
function getCookie(name) {
  if (typeof document === 'undefined') return null;
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

// Helper to set cookie value
function setCookie(name, value, days = 365) {
  if (typeof document === 'undefined') return;
  const date = new Date();
  date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
  const expires = `expires=${date.toUTCString()}`;
  document.cookie = `${name}=${value};${expires};path=/`;
}

import { t } from './langStore.js';

function generateId() {
  return Math.random().toString(36).substring(2, 9);
}

// Get the master team object from cookies
export function getTeamData() {
  const cookieVal = getCookie(TEAM_COOKIE_NAME);
  if (cookieVal) {
    try {
      const parsed = JSON.parse(decodeURIComponent(cookieVal));
      
      // Migration: if it's a flat array (legacy format), wrap it in the new format
      if (Array.isArray(parsed)) {
        const migratedData = {
          activeTeamId: 'legacy-team',
          teams: [
            { id: 'legacy-team', name: `${t('team_default')} 1`, members: parsed }
          ]
        };
        saveTeamData(migratedData);
        return migratedData;
      }
      
      return parsed;
    } catch (e) {
      console.error('Failed to parse team cookie:', e);
    }
  }
  
  // Default fresh state
  const defaultTeamId = generateId();
  return {
    activeTeamId: defaultTeamId,
    teams: [
      { id: defaultTeamId, name: `${t('team_default')} 1`, members: [] }
    ]
  };
}

// Save the master team object
function saveTeamData(data) {
  setCookie(TEAM_COOKIE_NAME, encodeURIComponent(JSON.stringify(data)));
  // Dispatch global event when data is saved to sync multiple components
  if (typeof window !== 'undefined') {
    window.dispatchEvent(new CustomEvent('team-data-updated'));
  }
}

export function getAllTeams() {
  return getTeamData().teams;
}

export function getActiveTeam() {
  const data = getTeamData();
  return data.teams.find(t => t.id === data.activeTeamId) || null;
}

export function getActiveTeamId() {
  return getTeamData().activeTeamId;
}

// Legacy alias to keep components from breaking until they are fully migrated
export function getTeam() {
  return getActiveTeam().members;
}

// Ensure the store is globally available
if (typeof window !== 'undefined') {
  window.teamStore = {
    getTeamData,
    saveTeamData,
    createTeam,
    deleteTeam,
    setActiveTeam,
    renameActiveTeam,
    addToTeam,
    removeFromTeam,
    isInTeam,
    getActiveTeam,
    updatePokemonConfig
  };
}

export function createTeam() {
  const data = getTeamData();
  const newTeam = {
    id: generateId(),
    name: `${t('team_default')} ${data.teams.length + 1}`,
    members: []
  };
  data.teams.push(newTeam);
  data.activeTeamId = newTeam.id;
  saveTeamData(data);
  return newTeam.id;
}

export function deleteTeam(id) {
  const data = getTeamData();
  if (data.teams.length <= 1) {
    return { success: false, message: 'You must keep at least one team.' };
  }
  
  data.teams = data.teams.filter(t => t.id !== id);
  if (data.activeTeamId === id) {
    data.activeTeamId = data.teams[0].id;
  }
  saveTeamData(data);
  return { success: true };
}

export function setActiveTeam(id) {
  const data = getTeamData();
  if (data.teams.some(t => t.id === id)) {
    data.activeTeamId = id;
    saveTeamData(data);
  }
}

export function renameActiveTeam(newName) {
  const data = getTeamData();
  const team = data.teams.find(t => t.id === data.activeTeamId);
  if (team) {
    team.name = newName;
    saveTeamData(data);
  }
}

// Add a pokemon to the ACTIVE team
export function addToTeam(pokemon) {
  const data = getTeamData();
  const activeTeam = data.teams.find(t => t.id === data.activeTeamId);
  
  if (!activeTeam) return { success: false, message: 'No active team.' };

  if (activeTeam.members.length >= MAX_TEAM_SIZE) {
    return { success: false, message: 'Your team is full (max 6 Pokémon)!' };
  }
  
  const isDuplicate = activeTeam.members.some(p => p.id === pokemon.id);
  if (isDuplicate) {
    return { success: false, message: 'You already have this Pokémon (or another form of it) in your team.' };
  }

  activeTeam.members.push({
    ...pokemon,
    ability: pokemon.ability || null,
    item: pokemon.item || null,
    nature: pokemon.nature || '25',
    moves: pokemon.moves || [null, null, null, null],
    evs: pokemon.evs || {
      hp: 0,
      attack: 0,
      defense: 0,
      'special-attack': 0,
      'special-defense': 0,
      speed: 0
    }
  });
  saveTeamData(data);
  return { success: true, message: 'Pokémon added to team!' };
}

// Remove a pokemon from the ACTIVE team by ID and form
export function removeFromTeam(id, form) {
  const data = getTeamData();
  const activeTeam = data.teams.find(t => t.id === data.activeTeamId);
  
  if (!activeTeam) return false;

  // Form is intentionally ignored to treat all forms of the same Pokémon as mutually exclusive
  const index = activeTeam.members.findIndex(p => p.id === id);
  if (index !== -1) {
    activeTeam.members.splice(index, 1);
    saveTeamData(data);
    return true;
  }
  return false;
}

// Check if a pokemon is in the ACTIVE team
export function isInTeam(id, form) {
  const activeTeam = getActiveTeam();
  // Form is intentionally ignored
  return activeTeam.members.some(p => p.id === id);
}

// Update pokemon config in the ACTIVE team
export function updatePokemonConfig(id, form, config) {
  const data = getTeamData();
  const activeTeam = data.teams.find(t => t.id === data.activeTeamId);
  
  if (!activeTeam) return false;

  const index = activeTeam.members.findIndex(p => p.id === id && p.form === form);
  if (index !== -1) {
    activeTeam.members[index] = {
      ...activeTeam.members[index],
      ...config
    };
    saveTeamData(data);
    return true;
  }
  return false;
}

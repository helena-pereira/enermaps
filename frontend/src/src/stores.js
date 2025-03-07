import {writable} from 'svelte/store';

export const datasetsStore = writable([]);
export const datasetTopicsStore = writable([]);

export const areaSelectionStore = writable(null);
export const areaSelectionLayerStore = writable(null);

export const layersStore = writable([]);
export const selectedLayerStore = writable(null);

export const tasksStore = writable([]);

export const isCMPaneActiveStore = writable(true);

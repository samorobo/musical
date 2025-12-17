<script setup lang="ts">
import { ref } from 'vue';
import { Music, Loader2, Play, Disc, ListMusic } from 'lucide-vue-next';

interface Song {
  song: string;
  artist: string;
}

interface PlaylistResponse {
  genre: string;
  message: string;
  playlist: Song[];
}

const genres = [
  'Pop', 'Rock', 'Jazz', 'Hip Hop', 'R&B', 
  'Country', 'Classical', 'Electronic', 'Reggae', 
  'Blues', 'Afrobeats', 'K-Pop', 'Indie', 'Metal'
];

const selectedGenre = ref('');
const playlist = ref<Song[]>([]);
const loading = ref(false);
const error = ref('');
const toastData = ref<{ message: string; type: 'success' | 'error' } | null>(null);

const showToast = (message: string, type: 'success' | 'error') => {
  toastData.value = { message, type };
  setTimeout(() => {
    toastData.value = null;
  }, 3000);
};

const generatePlaylist = async () => {
  if (!selectedGenre.value) {
    showToast('Please select a genre first', 'error');
    return;
  }

  loading.value = true;
  error.value = '';
  playlist.value = [];

  try {
    const response = await fetch('http://127.0.0.1:5000/api/generate-playlist', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ genre: selectedGenre.value }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || 'Failed to generate playlist');
    }

    const result = data as PlaylistResponse;
    playlist.value = result.playlist;
    showToast(result.message, 'success');
  } catch (err: any) {
    console.error('Error generating playlist:', err);
    error.value = err.message || 'An unexpected error occurred';
    showToast(error.value, 'error');
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="min-h-screen bg-background text-foreground flex flex-col items-center justify-center p-6 relative overflow-hidden font-sans">
    <!-- Background Decor -->
    <div class="absolute top-0 left-0 w-full h-full overflow-hidden -z-10 pointer-events-none opacity-20">
      <div class="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-primary blur-[120px]"></div>
      <div class="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-secondary blur-[120px]"></div>
    </div>

    <!-- Toast Notification -->
    <Transition
      enter-active-class="transition ease-out duration-300"
      enter-from-class="transform translate-y-4 opacity-0"
      enter-to-class="transform translate-y-0 opacity-100"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="transform translate-y-0 opacity-100"
      leave-to-class="transform translate-y-4 opacity-0"
    >
      <div 
        v-if="toastData" 
        class="fixed top-6 right-6 z-50 px-6 py-4 rounded-xl shadow-2xl border flex items-center gap-3"
        :class="toastData.type === 'error' ? 'bg-destructive/10 border-destructive text-destructive' : 'bg-primary/10 border-primary text-primary'"
      >
        <div class="w-2 h-2 rounded-full" :class="toastData.type === 'error' ? 'bg-destructive' : 'bg-primary'"></div>
        <span class="font-medium">{{ toastData.message }}</span>
      </div>
    </Transition>

    <div class="max-w-6xl w-full grid lg:grid-cols-2 gap-16 items-center">
      
      <!-- Input Section -->
      <div class="space-y-10 text-center lg:text-left">
        <div class="space-y-6">
          <div class="inline-flex items-center justify-center lg:justify-start gap-2 text-primary font-bold tracking-wider uppercase text-sm">
            <Music class="w-4 h-4" />
            <span>AI Music Generator</span>
          </div>
          <h1 class="text-5xl lg:text-7xl font-black tracking-tight leading-[1.1]">
            Curate Your <br />
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-primary via-accent to-secondary">Perfect Vibe</span>
          </h1>
          <p class="text-muted-foreground text-xl max-w-md mx-auto lg:mx-0 leading-relaxed">
            Select a genre and let our AI instantly craft a tailored 5-song playlist just for you.
          </p>
        </div>

        <div class="space-y-4 max-w-md mx-auto lg:mx-0">
          <div class="flex flex-col sm:flex-row gap-4">
            <div class="relative flex-1 group">
              <select 
                v-model="selectedGenre"
                class="w-full h-16 pl-6 pr-12 bg-card border-none ring-1 ring-border rounded-2xl appearance-none focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all cursor-pointer font-medium text-lg shadow-sm"
              >
                <option value="" disabled selected>Select a Genre</option>
                <option v-for="genre in genres" :key="genre" :value="genre">{{ genre }}</option>
              </select>
              <div class="absolute right-5 top-1/2 -translate-y-1/2 pointer-events-none text-muted-foreground group-hover:text-primary transition-colors">
                <ListMusic class="w-6 h-6" />
              </div>
            </div>

            <button 
              @click="generatePlaylist"
              :disabled="loading"
              class="h-16 px-10 bg-primary text-primary-foreground font-bold text-lg rounded-2xl hover:bg-primary/90 hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50 disabled:pointer-events-none flex items-center justify-center gap-3 shadow-xl shadow-primary/20"
            >
              <Loader2 v-if="loading" class="w-6 h-6 animate-spin" />
              <span v-else>Generate</span>
              <Play v-if="!loading" class="w-5 h-5 fill-current" />
            </button>
          </div>
          <p v-if="!selectedGenre && !loading" class="text-sm text-muted-foreground italic pl-2">
            * Please select a genre to start
          </p>
        </div>
      </div>

      <!-- Result Section -->
      <div class="relative w-full aspect-[4/5] lg:aspect-square max-h-[600px]">
        
        <!-- Empty State -->
        <div 
          v-if="playlist.length === 0 && !loading" 
          class="absolute inset-0 flex flex-col items-center justify-center text-muted-foreground border-2 border-dashed border-border rounded-[2.5rem] bg-card/50 backdrop-blur-sm p-8 text-center gap-6"
        >
          <div class="w-32 h-32 rounded-full bg-muted/20 flex items-center justify-center">
            <Disc class="w-16 h-16 opacity-40" />
          </div>
          <p class="font-medium text-lg max-w-xs">Your curated playlist will appear here. Pick a genre to get started!</p>
        </div>

        <!-- Loading Skeleton -->
        <div v-if="loading" class="w-full h-full p-8 border border-border rounded-[2.5rem] bg-card/80 backdrop-blur-md flex flex-col gap-6 shadow-2xl">
           <div class="h-8 w-1/2 bg-muted/20 rounded-lg animate-pulse mb-4"></div>
           <div v-for="n in 5" :key="n" class="w-full h-24 bg-muted/10 rounded-2xl animate-pulse flex items-center px-6 gap-6 border border-border/50">
              <div class="w-16 h-16 bg-muted/20 rounded-xl"></div>
              <div class="flex-1 space-y-3">
                <div class="w-3/4 h-5 bg-muted/20 rounded"></div>
                <div class="w-1/2 h-4 bg-muted/10 rounded"></div>
              </div>
           </div>
        </div>

        <!-- Playlist Display -->
        <div 
          v-if="playlist.length > 0 && !loading"
          class="w-full h-full flex flex-col p-8 border border-border rounded-[2.5rem] bg-card/90 backdrop-blur-xl shadow-2xl relative overflow-hidden"
        >
          <!-- Blob decoration inside card -->
          <div class="absolute top-0 right-0 w-64 h-64 bg-primary/10 blur-[80px] rounded-full pointer-events-none"></div>

          <div class="relative z-10 mb-8 flex justify-between items-end border-b border-border/50 pb-6">
             <div>
               <p class="text-sm font-bold tracking-widest text-primary uppercase mb-1">Generated Mix</p>
               <h3 class="font-black text-3xl">{{ selectedGenre }} Vibes</h3>
             </div>
             <div class="w-12 h-12 rounded-full bg-primary/10 text-primary flex items-center justify-center">
                <Music class="w-6 h-6" />
             </div>
          </div>

          <div class="flex-1 overflow-y-auto space-y-3 -mr-4 pr-4 custom-scrollbar">
            <div 
              v-for="(track, index) in playlist" 
              :key="index"
              class="group flex items-center gap-5 p-4 rounded-2xl hover:bg-white/5 transition-all border border-transparent hover:border-white/10"
            >
              <span class="w-10 h-10 flex items-center justify-center font-mono text-muted-foreground group-hover:text-primary font-bold text-xl opacity-50">
                0{{ index + 1 }}
              </span>
              
              <div class="w-16 h-16 rounded-xl bg-gradient-to-br from-gray-800 to-black flex items-center justify-center shadow-lg group-hover:scale-105 transition-transform border border-white/5">
                <Music class="w-8 h-8 text-white/20 group-hover:text-primary transition-colors" />
              </div>

              <div class="flex-1 min-w-0">
                <h4 class="font-bold text-foreground truncate group-hover:text-primary transition-colors text-xl">
                  {{ track.song }}
                </h4>
                <p class="text-base text-muted-foreground truncate font-medium mt-1">
                  {{ track.artist }}
                </p>
              </div>
            </div>
          </div>
          
          <div class="mt-6 pt-6 border-t border-border/50 text-center text-xs text-muted-foreground font-medium uppercase tracking-widest">
            AI Generated • {{ new Date().toLocaleDateString() }}
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: hsl(var(--border));
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: hsl(var(--muted-foreground));
}
</style>

<script setup lang="ts">
import { ref, computed } from "vue"
import {
  Music2,
  AlertCircle,
  Disc3,
} from "lucide-vue-next"

const GENRES = [
  "Pop",
  "Jazz",
  "Rock",
  "Hip-Hop",
  "Electronic",
  "Classical",
  "R&B",
  "Indie",
] as const

type Genre = (typeof GENRES)[number]

interface Track {
  id: string
  artist: string
  title: string
}

const genre = ref<Genre | "">("")
const tracks = ref<Track[] | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

const hasPlaylist = computed(() => !!tracks.value?.length)

async function handleGenerate() {
  if (!genre.value || loading.value) return

  loading.value = true
  error.value = null

  try {
    await new Promise((r) => setTimeout(r, 700))

    const res = await fetch(`/api/playlist/${encodeURIComponent(genre.value)}`)
    if (!res.ok) throw new Error("Failed to generate playlist")

    const data = await res.json()
    tracks.value = data.playlist.slice(0, 5)
  } catch {
    error.value =
      "Something went wrong while generating your playlist. Please try again."
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div
    class="min-h-screen w-full bg-background text-foreground flex items-center justify-center px-4"
  >
    <!-- Background gradients -->
    <div
      class="absolute inset-0 -z-10 bg-[radial-gradient(circle_at_top,_rgba(255,107,74,0.16),transparent_55%),radial-gradient(circle_at_bottom,_rgba(168,197,166,0.12),transparent_55%)]"
    ></div>

    <div
      class="absolute inset-0 -z-10 opacity-[0.06] mix-blend-soft-light bg-cover bg-center"
      style="background-image:url('https://images.unsplash.com/photo-1518831959415-50ff11b8a8f1?auto=format&fit=crop&w=1200&q=40')"
    ></div>

    <div class="relative w-full max-w-[680px] py-16 md:py-24">
      <!-- Header -->
      <header class="mb-12">
        <p
          class="font-mono text-xs uppercase tracking-[0.22em] text-muted-foreground mb-4"
        >
          AI-powered · Genre-first
        </p>
        <h1
          class="font-serif text-[2.75rem] md:text-[4.5rem] leading-tight"
        >
          Curate the soundtrack<br />
          to your next obsession.
        </h1>
        <p class="mt-4 text-muted-foreground">
          Pick a genre and generate a five-track snapshot.
        </p>
      </header>

      <!-- Controls -->
      <section class="flex flex-col md:flex-row gap-4 mb-10">
        <div class="flex-1">
          <label
            class="block text-xs uppercase tracking-[0.22em] text-muted-foreground mb-2"
          >
            Genre
          </label>

          <select
            v-model="genre"
            class="h-14 w-full rounded-full border border-border bg-card px-5"
          >
            <option value="" disabled>Select a genre</option>
            <option v-for="g in GENRES" :key="g" :value="g">
              {{ g }}
            </option>
          </select>
        </div>

        <button
          @click="handleGenerate"
          :disabled="!genre || loading"
          class="h-14 px-8 rounded-full bg-primary text-primary-foreground uppercase tracking-wide font-semibold disabled:opacity-60"
        >
          {{ loading ? "Generating…" : hasPlaylist ? "Regenerate" : "Generate" }}
        </button>
      </section>

      <!-- Error -->
      <div
        v-if="error"
        class="flex gap-3 rounded-xl border border-destructive/60 bg-destructive/10 px-4 py-3 text-sm"
      >
        <AlertCircle class="w-4 h-4" />
        <div>
          <p class="font-medium">We hit a sour note.</p>
          <p class="text-muted-foreground text-xs">
            {{ error }}
            <button
              class="ml-2 underline text-primary"
              @click="handleGenerate"
            >
              Retry
            </button>
          </p>
        </div>
      </div>

      <!-- Empty state -->
      <div
        v-if="!hasPlaylist && !error"
        class="mt-10 text-center border border-dashed rounded-2xl py-12"
      >
        <Music2 class="mx-auto mb-4 w-8 h-8 text-muted-foreground" />
        <h2 class="text-2xl font-serif">Your playlist awaits.</h2>
        <p class="text-muted-foreground mt-2">
          Select a genre and generate your tracks.
        </p>
      </div>

      <!-- Playlist -->
      <div v-if="hasPlaylist" class="mt-10 space-y-3">
        <div
          v-for="(track, i) in tracks"
          :key="track.id"
          class="flex items-center gap-4 rounded-xl border bg-card px-4 py-4"
        >
          <Disc3 class="w-5 h-5 text-muted-foreground" />
          <div class="flex-1">
            <p class="text-xs uppercase text-muted-foreground">
              {{ String(i + 1).padStart(2, "0") }} · {{ genre }}
            </p>
            <p class="font-semibold">{{ track.artist }}</p>
            <p class="text-sm text-muted-foreground">{{ track.title }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

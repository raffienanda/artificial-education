<template>
  <!-- Number Line SVG matching the reference design -->
  <svg viewBox="0 0 400 120" class="w-full" xmlns="http://www.w3.org/2000/svg">
    <!-- Main line -->
    <line x1="30" y1="70" x2="370" y2="70" stroke="#CBD5E1" stroke-width="2" />

    <!-- Tick marks and labels -->
    <g v-for="n in 7" :key="n">
      <line
        :x1="30 + (n - 1) * 56.67"
        y1="63"
        :x2="30 + (n - 1) * 56.67"
        y2="77"
        stroke="#94A3B8"
        stroke-width="1.5"
      />
      <text
        :x="30 + (n - 1) * 56.67"
        y="95"
        text-anchor="middle"
        class="text-xs fill-gray-600 dark:fill-gray-400"
        font-size="13"
        font-family="Inter, sans-serif"
      >
        {{ n - 4 }}
      </text>
    </g>

    <!-- Arrow heads -->
    <polygon points="26,70 34,66 34,74" fill="#94A3B8" />
    <polygon points="374,70 366,66 366,74" fill="#94A3B8" />

    <!-- Red arc: 0 to -3 (bottom) -->
    <path
      d="M 200,75 Q 200,105 86.67,105 Q 30,105 30,75"
      fill="none"
      stroke="#EF4444"
      stroke-width="2"
      stroke-dasharray="4,3"
    />
    <!-- Red arrow tip on the arc -->
    <polygon points="30,78 25,72 35,72" fill="#EF4444" />
    <!-- Red label -->
    <text x="110" y="115" text-anchor="middle" fill="#EF4444" font-size="13" font-weight="600" font-family="Inter, sans-serif">
      −3
    </text>

    <!-- Blue arc: -3 to -1 (top) -->
    <path
      d="M 30,65 Q 30,30 86.67,30 Q 143.33,30 143.33,65"
      fill="none"
      stroke="#2563EB"
      stroke-width="2"
      stroke-dasharray="4,3"
    />
    <!-- Blue arrow tip -->
    <polygon points="143.33,62 148,68 138,68" fill="#2563EB" />
    <!-- Blue label -->
    <text x="86.67" y="22" text-anchor="middle" fill="#2563EB" font-size="13" font-weight="600" font-family="Inter, sans-serif">
      +2
    </text>

    <!-- Dot at 0 -->
    <circle cx="200" cy="70" r="4" fill="#2563EB" />
    <!-- Dot at -3 -->
    <circle cx="30" cy="70" r="4" fill="#EF4444" />
    <!-- Dot at -1 -->
    <circle cx="143.33" cy="70" r="4" fill="#2563EB" />
  </svg>
</template>

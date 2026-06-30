<template>
  <div class="bg-gradient-to-r from-primary-50 to-blue-50 dark:from-primary-900/20 dark:to-blue-900/20 rounded-xl p-4 border border-primary-100 dark:border-primary-800">
    <div class="flex items-start gap-3">
      <div class="text-xl mt-0.5">💡</div>
      <div>
        <h4 class="text-sm font-semibold text-primary-800 dark:text-primary-300 mb-1">AI Recommendation</h4>
        <p class="text-xs text-primary-700 dark:text-primary-400 mb-2 leading-relaxed">
          {{ recommendation.message }}
        </p>
        
        <div class="flex flex-wrap gap-1.5 mb-3">
          <BaseBadge 
            v-for="topic in recommendation.weakTopics" 
            :key="topic.id" 
            variant="warning" 
            size="xs"
          >
            Review: {{ topic.subtopic }}
          </BaseBadge>
        </div>

        <div class="flex items-center justify-between">
          <span class="text-xs font-medium text-primary-600 dark:text-primary-400">
            Est. time: {{ recommendation.totalEstimatedTime }}
          </span>
          <BaseButton variant="primary" size="sm" class="py-1 px-3 text-xs">
            Start Practice
          </BaseButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * RecommendationCard — AI-generated learning recommendation based on BKT
 */
import BaseBadge from '@/components/common/BaseBadge.vue'
import BaseButton from '@/components/common/BaseButton.vue'

defineProps({
  recommendation: { type: Object, required: true },
})
</script>

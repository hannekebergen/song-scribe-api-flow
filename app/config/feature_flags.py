"""
Feature Flags voor Database-Driven Prompts
Veilige rollout van nieuwe features met A/B testing mogelijkheden
"""

import os
from typing import Dict, Any, Optional
from enum import Enum

class FeatureFlag(Enum):
    """Available feature flags"""
    DATABASE_PROMPTS = "database_prompts"
    SUNO_OPTIMIZATION = "suno_optimization"
    PROMPT_CACHING = "prompt_caching"
    ADVANCED_THEMA_MATCHING = "advanced_thema_matching"

class FeatureFlagManager:
    """Manages feature flags with environment variable support"""
    
    def __init__(self):
        self._flags = self._load_flags()
    
    def _load_flags(self) -> Dict[str, Any]:
        """Load feature flags from environment variables and defaults"""
        return {
            # Database-driven prompt generation
            FeatureFlag.DATABASE_PROMPTS.value: {
                "enabled": os.getenv("FEATURE_DATABASE_PROMPTS", "true").lower() == "true",
                "rollout_percentage": int(os.getenv("FEATURE_DATABASE_PROMPTS_ROLLOUT", "100")),
                "description": "Use database elements for prompt generation",
                "fallback_on_error": True
            },
            
            # Suno.ai optimized prompts
            FeatureFlag.SUNO_OPTIMIZATION.value: {
                "enabled": os.getenv("FEATURE_SUNO_OPTIMIZATION", "false").lower() == "true",
                "rollout_percentage": int(os.getenv("FEATURE_SUNO_OPTIMIZATION_ROLLOUT", "0")),
                "description": "Enable Suno.ai optimized prompt formatting",
                "fallback_on_error": True
            },
            
            # Prompt caching for performance
            FeatureFlag.PROMPT_CACHING.value: {
                "enabled": os.getenv("FEATURE_PROMPT_CACHING", "false").lower() == "true",
                "rollout_percentage": int(os.getenv("FEATURE_PROMPT_CACHING_ROLLOUT", "0")),
                "description": "Cache generated prompts for better performance",
                "fallback_on_error": False
            },
            
            # Advanced thema matching
            FeatureFlag.ADVANCED_THEMA_MATCHING.value: {
                "enabled": os.getenv("FEATURE_ADVANCED_THEMA_MATCHING", "true").lower() == "true",
                "rollout_percentage": int(os.getenv("FEATURE_ADVANCED_THEMA_MATCHING_ROLLOUT", "100")),
                "description": "Use fuzzy matching for thema string to ID conversion",
                "fallback_on_error": True
            }
        }
    
    def is_enabled(self, flag: FeatureFlag, user_id: Optional[str] = None) -> bool:
        """
        Check if a feature flag is enabled for a user
        
        Args:
            flag: The feature flag to check
            user_id: Optional user ID for percentage rollout
            
        Returns:
            True if feature is enabled for this user
        """
        flag_config = self._flags.get(flag.value, {})
        
        if not flag_config.get("enabled", False):
            return False
        
        rollout_percentage = flag_config.get("rollout_percentage", 0)
        
        if rollout_percentage >= 100:
            return True
        elif rollout_percentage <= 0:
            return False
        else:
            # Simple hash-based rollout if user_id provided
            if user_id:
                hash_value = hash(user_id) % 100
                return hash_value < rollout_percentage
            else:
                # For requests without user_id, use global percentage
                return rollout_percentage >= 50  # Default threshold
    
    def get_flag_config(self, flag: FeatureFlag) -> Dict[str, Any]:
        """Get complete configuration for a feature flag"""
        return self._flags.get(flag.value, {})
    
    def should_fallback_on_error(self, flag: FeatureFlag) -> bool:
        """Check if feature should fallback to old behavior on error"""
        return self._flags.get(flag.value, {}).get("fallback_on_error", True)
    
    def get_all_flags(self) -> Dict[str, Dict[str, Any]]:
        """Get all feature flags for admin/debugging"""
        return self._flags.copy()

# Global instance
feature_flags = FeatureFlagManager()

# Convenience functions
def is_database_prompts_enabled(user_id: Optional[str] = None) -> bool:
    """Check if database-driven prompts are enabled"""
    return feature_flags.is_enabled(FeatureFlag.DATABASE_PROMPTS, user_id)

def is_suno_optimization_enabled(user_id: Optional[str] = None) -> bool:
    """Check if Suno.ai optimization is enabled"""
    return feature_flags.is_enabled(FeatureFlag.SUNO_OPTIMIZATION, user_id)

def should_cache_prompts(user_id: Optional[str] = None) -> bool:
    """Check if prompt caching is enabled"""
    return feature_flags.is_enabled(FeatureFlag.PROMPT_CACHING, user_id)

def is_advanced_thema_matching_enabled(user_id: Optional[str] = None) -> bool:
    """Check if advanced thema matching is enabled"""
    return feature_flags.is_enabled(FeatureFlag.ADVANCED_THEMA_MATCHING, user_id) 
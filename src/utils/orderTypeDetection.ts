/**
 * Utility functions for detecting order types based on product information
 */

import { Order } from '@/types';

export interface OrderTypeInfo {
  type: string;
  badge: 'standaard' | 'spoed' | 'upsell' | 'order-bump';
  priority: number; // Higher number = higher priority for display
}

/**
 * Detect the order type based on product information
 */
export function detectOrderType(order: Order): OrderTypeInfo {
  // Get products from raw_data or fallback to legacy field
  const products = order.raw_data?.products || order.products || [];
  
  if (products.length === 0) {
    return {
      type: 'Onbekend',
      badge: 'standaard',
      priority: 0
    };
  }

  // Find the main product (highest priority)
  let mainOrderType: OrderTypeInfo | null = null;
  const additionalTypes: string[] = [];

  for (const product of products) {
    const productId = product.id;
    const pivotType = product.pivot?.type;
    const title = product.title || product.name || '';

    // Determine product type
    let orderType: OrderTypeInfo;

    // Main products (highest priority)
    if (productId === 274588) {
      orderType = {
        type: 'Standaard 72u',
        badge: 'standaard',
        priority: 100
      };
    } else if (productId === 289456) {
      orderType = {
        type: 'Spoed 24u',
        badge: 'spoed',
        priority: 200
      };
    }
    // Upsells
    else if (pivotType === 'upsell') {
      if (productId === 294847) {
        orderType = {
          type: 'Revisie',
          badge: 'upsell',
          priority: 50
        };
      } else if (productId === 299107) {
        orderType = {
          type: 'Soundtrack Bundel',
          badge: 'upsell',
          priority: 50
        };
      } else if (productId === 299088) {
        orderType = {
          type: 'Extra Coupletten',
          badge: 'upsell',
          priority: 50
        };
      } else {
        orderType = {
          type: 'Upsell',
          badge: 'upsell',
          priority: 50
        };
      }
    }
    // Order-bumps
    else if (pivotType === 'order-bump') {
      if (productId === 294792) {
        orderType = {
          type: 'Karaoke Track',
          badge: 'order-bump',
          priority: 30
        };
      } else if (productId === 299891) {
        orderType = {
          type: 'Engelstalig',
          badge: 'order-bump',
          priority: 30
        };
      } else {
        orderType = {
          type: 'Order-bump',
          badge: 'order-bump',
          priority: 30
        };
      }
    }
    // Fallback based on title analysis
    else {
      if (title.includes('24') || title.toLowerCase().includes('24u') || title.toLowerCase().includes('24 u')) {
        orderType = {
          type: 'Spoed 24u',
          badge: 'spoed',
          priority: 200
        };
      } else if (title.includes('72') || title.toLowerCase().includes('72u') || title.toLowerCase().includes('72 u')) {
        orderType = {
          type: 'Standaard 72u',
          badge: 'standaard',
          priority: 100
        };
      } else {
        orderType = {
          type: 'Onbekend',
          badge: 'standaard',
          priority: 0
        };
      }
    }

    // Keep track of main order type (highest priority)
    if (!mainOrderType || orderType.priority > mainOrderType.priority) {
      if (mainOrderType) {
        additionalTypes.push(mainOrderType.type);
      }
      mainOrderType = orderType;
    } else {
      additionalTypes.push(orderType.type);
    }
  }

  // If we have additional types, append them to the main type
  if (additionalTypes.length > 0) {
    return {
      ...mainOrderType!,
      type: `${mainOrderType!.type} + ${additionalTypes.join(', ')}`
    };
  }

  return mainOrderType || {
    type: 'Onbekend',
    badge: 'standaard',
    priority: 0
  };
}

/**
 * Get a display-friendly order type string
 */
export function getOrderTypeDisplay(order: Order): string {
  const orderTypeInfo = detectOrderType(order);
  return orderTypeInfo.type;
}

/**
 * Get the badge type for styling
 */
export function getOrderTypeBadge(order: Order): 'standaard' | 'spoed' | 'upsell' | 'order-bump' {
  const orderTypeInfo = detectOrderType(order);
  return orderTypeInfo.badge;
}

/**
 * Check if an order is a spoed (urgent) order
 */
export function isSpeedOrder(order: Order): boolean {
  const orderTypeInfo = detectOrderType(order);
  return orderTypeInfo.badge === 'spoed';
} 
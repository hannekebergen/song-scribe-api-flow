declare module 'lucide-react' {
  import { ComponentType } from 'react';

  export interface IconProps {
    color?: string;
    size?: string | number;
    strokeWidth?: string | number;
    className?: string;
  }

  export const Download: ComponentType<IconProps>;
  export const AlertCircle: ComponentType<IconProps>;
  export const CheckCircle: ComponentType<IconProps>;
  export const Loader2: ComponentType<IconProps>;
  // Add other icons as needed
}

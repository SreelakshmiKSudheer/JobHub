import type {
    ButtonColor,
    ButtonDirection,
    ButtonSize,
    ButtonVariant,
} from "../../../types/button.types";

export const variants: Record<ButtonVariant, string> = {
  filled:
    "border border-transparent",

  outline:
    "border border-2 bg-transparent",

  none:
    "border-0",
};

export const colors: Record<ButtonColor, Record<ButtonVariant, string>> = {
  primary: {
    filled:
      "bg-primary text-white hover:bg-primary hover:bg-primary-hover",

    outline:
      "border-primary text-primary hover:bg-primary hover:text-bg-alt",
  
    none:
      "text-primary hover:bg-primary/10"
    },

  secondary: {
    filled:
      "bg-secondary text-bg-alt hover:bg-secondary-hover ",

    outline:
      "border-secondary text-secondary hover:bg-secondary hover:text-bg-alt",
 
    none:
      "text-secondary hover:bg-secondary/10"
    },

  success: {
    filled:
      "bg-green-600 text-white hover:bg-green-700 ",

    outline:
      "border-green-600 text-green-600 hover:bg-green-50- hover:text-bg-alt",

    none:
      "text-green-600 hover:text-green-700"
  },

  danger: {
    filled:
      "bg-red-600 text-white hover:bg-red-700",

    outline:
      "border-red-600 text-red-600 hover:bg-red-50 ",
    none:
      "text-red-600 hover:text-red-700"
  },
};

export const sizes: Record<ButtonSize, string> = {
  sm: "px-3 py-2 text-sm",

  md: "px-5 py-2 text-base",

  lg: "px-6 py-3 text-lg",
};

export const directions: Record<ButtonDirection, string> = {
  row: "flex-row",
  col: "flex-col",
};
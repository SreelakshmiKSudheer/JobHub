import type {
  ButtonHTMLAttributes,
  ReactNode,
} from "react";

export type ButtonVariant = "filled" | "outline" | "none";

export type ButtonSize = "sm" | "md" | "lg";

export type ButtonColor =
  | "primary"
  | "secondary"
  | "danger"
  | "success";

export type IconPosition = "left" | "right";

export type ButtonDirection = "row" | "col";

export interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {
  text?: string | ReactNode;

  textClassName?: string;

  icon?: ReactNode;

  variant?: ButtonVariant;

  size?: ButtonSize;

  color?: ButtonColor;

  iconPosition?: IconPosition;

  iconDirection?: ButtonDirection;

  fullWidth?: boolean;

  loading?: boolean;

  onClick?: () => void;
}

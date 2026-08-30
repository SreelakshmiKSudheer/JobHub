import type { ButtonProps } from "../../../types/button.types";
import {
  variants,
  colors,
  sizes,
  directions,
} from "./ButtonVariant";

const Button = ({
  text,
  textClassName = "",
  icon,
  variant = "filled",
  size = "md",
  color = "primary",
  iconPosition = "left",
  iconDirection = "row",
  loading = false,
  fullWidth = false, // 1. Extract fullWidth from props
  className = "",
  disabled,
  type = "button",
  onClick,
  ...props
}: ButtonProps) => {
  return (
    <button
      type={type}
      disabled={disabled || loading}
      className={`
        /* 2. Dynamically apply width and flex classes */
        ${fullWidth ? "w-full flex" : "w-fit inline-flex"} 
        
        items-center
        justify-center
        gap-2
        transition-all
        duration-200
        font-medium
        cursor-pointer

        ${variants[variant]}
        ${colors[color][variant]}
        ${sizes[size]}
        ${directions[iconDirection]}

        ${
          disabled || loading
            ? "opacity-60 cursor-not-allowed"
            : ""
        }

        ${className}
      `}
      onClick={onClick}
      {...props}
    >
      {loading ? (
        <>
          <span>Loading...</span>
        </>
      ) : (
        <>
          {iconPosition === "left" && icon}

          {text && <span className={textClassName}>{text}</span>}

          {iconPosition === "right" && icon}
        </>
      )}
    </button>
  );
};

export default Button;
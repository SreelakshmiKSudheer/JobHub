import type { HeroBackgroundProps } from "../../../types/HeroBackground.types";

export const HeroBackground = ({
  image,
  alt = "",
  overlay = true,
}: HeroBackgroundProps) => {
  return (
    <div className="relative w-full h-full overflow-hidden">
      {overlay && (
        <div className="absolute inset-0 bg-bg/40 z-5 md:hidden"></div>
      )}
      
      <img 
        src={image} 
        alt={alt} 
        className="w-full h-full object-cover object-center opacity-60 md:rounded-2xl md:opacity-100" 
      />
    </div>
  );
};
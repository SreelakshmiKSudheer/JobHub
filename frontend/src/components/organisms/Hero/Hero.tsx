import { Play, Plus } from "lucide-react";
import { useNavigate } from "react-router";

import Button from "../../atoms/Button/Button";
import { Typography } from "../../atoms/Typography/Typography";
import { HeroBackground } from "../../molecules/HeroBackground/HeroBackground";

import type { HeroProps } from "../../../types/hero.types";

const Hero = ({
  backgroundImage,
  title,
  description,
  ctaText,
  ctaLink,
  socialProofs,
  direction = "ltr",
}: HeroProps) => {
  const navigate = useNavigate();

  return (
    <section 
      className={`relative w-full mx-auto overflow-hidden flex flex-col ${
        direction === "ltr" ? "md:flex-row" : "md:flex-row-reverse"
      } md:justify-between md:items-stretch py-16 md:py-15 min-h-[60vh]`}
    >
      
      {/* Content */}
      <div 
        className={`relative z-10 w-full md:w-3/5 flex flex-col justify-center ${
          direction === "ltr" ? "md:pr-10" : "md:pl-10"
        }`}
      >
        <div className="max-w-xl md:max-w-full">

          {/* Title */}
          <Typography
            variant="display"
            ashtml="h1"
            className="text-primary-hover"
          >
            {title}
          </Typography>

          {/* Description */}
          <Typography
            variant="body"
            ashtml="p"
            className="text-text text-sm md:text-lg mt-4"
          >
            {description}
          </Typography>

          {/* Social Proofs */}
          <div className="mt-2 md:mt-4 flex flex-wrap gap-3">
            {socialProofs?.map((proof, index) => (
              <div key={index} className="flex items-center gap-2">
                <Typography variant="caption" ashtml="p">
                  {proof}
                </Typography>
              </div>
            ))}
          </div>

          {/* Actions */}
          {ctaText && ctaLink && (
            <div className="mt-4 md:mt-6 flex flex-wrap gap-3">
            <Button
              variant="filled"
              text={ctaText}
              className="rounded-4xl px-0 md:px-6 py-0 md:py-2.5"
              onClick={() => navigate(ctaLink)}
            />
          </div>
          )}
        </div>
      </div>

      {/* Image / Background Wrapper */}
      <div className="absolute inset-0 md:relative md:z-0 md:w-2/5 md:flex">
        <HeroBackground image={backgroundImage} alt={title} overlay={true} />
      </div>

    </section>
  );
};

export default Hero;
export type HeroProps = {
  backgroundImage: string;
  title: string;
  description: string;
  ctaText?: string;
  ctaLink?: string;
  socialProofs?: string[];
  direction?: "ltr" | "rtl";
};
import type { FeatureCardProps } from "../../../types/featurecard.types";

const FeatureCard = ({ title, description, icon }: FeatureCardProps) => {
  return (
    <div className="bg-bg-alt w-full md:w-3/13 shadow-primary/30 shadow-md hover:shadow-lg hover:scale-105 transition-all cursor-pointer duration-300 rounded-2xl">
      {icon && (
        <div className="w-full bg-accent/70 h-30 flex items-center justify-center mb-2 rounded-t-2xl overflow-hidden">
          <img 
            src={icon} 
            alt={title} 
            className="w-[60%] h-full object-cover object-center" 
          />
        </div>
      )}
      <div className="px-4 md:px-6 py-2 md:py-4 bg-bg-alt rounded-b-2xl ">
        <h3 className="text-xl md:text-2xl font-bold mb-2 text-primary">{title}</h3>
        <p className="text-text-alt">{description}</p>
      </div>
    </div>
  );
};

export default FeatureCard;
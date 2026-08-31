import React from "react";
import Hero from "../../components/organisms/Hero/Hero";
import FeatureCard from "../../components/molecules/FeatureCard/FeatureCard";
import { Typography } from "../../components/atoms/Typography/Typography";
import Accordian from "../../components/molecules/Accordian/Accordian";

import { heroData1, heroData2, heroData3 } from "../../data/LandingPage/Hero";
import { featureData } from "../../data/LandingPage/Features";
import { faqData } from "../../data/LandingPage/Faq";
import FAQSection from "../../components/organisms/FAQSection.tsx/FAQSection";

const LandingPage = () => {
  return (
    <div className="w-full flex flex-col">
      {/* Hero Section */}
      <div id="home">
        <Hero {...heroData1} />
      </div>

      {/* Features */}
      <div id="features" className="w-full flex flex-col gap-2">
        <Typography variant="heading" className="text-primary-hover text-center">
          Features
        </Typography>
        <div className="w-full flex flex-wrap justify-between gap-4 mt-4">
          {featureData.map((feature, index) => (
            <FeatureCard
              key={index}
              title={feature.title}
              description={feature.description}
              icon={feature.icon}
            />
          ))}
        </div>
      </div>

      <div >
        <Hero
          title={heroData2.title}
          description={heroData2.description}
          backgroundImage={heroData2.backgroundImage}
          socialProofs={heroData2.socialProofs}
          direction={heroData2.direction}
        />
      </div>

      {/* FAQ */}
      <div id="about" className="w-full flex flex-col gap-2">
        <Typography variant="heading" className="text-primary-hover text-center">
          Frequently Asked Questions
        </Typography>
        <FAQSection />
      </div>

      {/* Final CTA */}
      <div>
        <Hero title={heroData3.title} description={heroData3.description} ctaText={heroData3.ctaText} ctaLink={heroData3.ctaLink} socialProofs={heroData3.socialProofs} backgroundImage={heroData3.backgroundImage} />
      </div>
    </div>
  );
};

export default LandingPage;

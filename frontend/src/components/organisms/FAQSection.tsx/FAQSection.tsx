import { useState } from 'react';
import Accordian from '../../molecules/Accordian/Accordian';
import { faqData } from '../../../data/LandingPage/Faq';

const FAQSection = () => {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const toggleAccordion = (index: number) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <div className="w-full flex flex-col items-center justify-center gap-4 mt-6">
      {faqData.map((faq, index) => (
        <Accordian
          key={index}
          title={faq.title}
          content={faq.content}
          isOpen={openIndex === index}
          onClick={() => toggleAccordion(index)}
        />
      ))}
    </div>
  );
};

export default FAQSection;

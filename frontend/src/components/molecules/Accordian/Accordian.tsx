import type { AccordianProps } from '../../../types/accordian.types'
import { ChevronDown } from 'lucide-react'

const Accordian = ({ title, content, isOpen, onClick }: AccordianProps) => {
  return (
    <div className="w-full md:w-[80%] flex flex-col items-center">
      <div 
        onClick={onClick}
        className={`bg-bg-alt w-full p-6 flex justify-between items-center border border-accent/20 text-text text-lg font-semibold shadow-md shadow-accent/20 hover:shadow-lg hover:scale-[1.01] transition-all cursor-pointer ${isOpen ? 'rounded-t-xl' : 'rounded-xl'}`}
      >
        {title}
        <span className="ml-2">
           <ChevronDown className={`transition-transform duration-300 ${isOpen ? "rotate-180" : ""}`} />
        </span>
      </div>
      
      {isOpen && (
        <div className="bg-accent/5 w-full p-6 border border-accent/30 border-t-0 rounded-b-xl">
          {content}
        </div>
      )}
    </div>
  )
}

export default Accordian
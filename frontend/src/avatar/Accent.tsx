import type { AccentType } from '../events/eventTypes';
import accentQuestionMarks from '../assets/avatar/accent-question-marks.png';
import accentDashes from '../assets/avatar/accent-dashes.png';
import accentZzz from '../assets/avatar/accent-zzz.png';
import accentHuff from '../assets/avatar/accent-huff.png';

const accentImages: Record<Exclude<AccentType, null>, string> = {
  questionMarks: accentQuestionMarks,
  sparkles: accentDashes,
  zzz: accentZzz,
  huff: accentHuff,
};

interface AccentProps {
  accent: AccentType | null;
}

export default function Accent({ accent }: AccentProps) {
  if (!accent) {
    return null;
  }

  return (
    <div className="accent" key={accent}>
      <img src={accentImages[accent]} alt={`Accent ${accent}`} />
    </div>
  );
}


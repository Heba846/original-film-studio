import React from 'react';
import {BellLetter, ContractPage, DivorceEnvelope, EhrChart, EvidenceChain, LegalPadTerms, Ledger, LotEvidence, PhoneNote, PocketSchedule, Subpoena} from './Evidence';
import {AprilEpilogue, ArrestTransition, CaseWeb, Countdown, DebtBeat, EvidenceRecap, GarageMap, ResusTimer} from './NarrativeGraphics';

/** component name (media_manifest.json shots[].component) -> React component */
export const CODE_COMPONENTS: Record<string, React.FC<any>> = {
  EhrChart, Subpoena, LegalPadTerms, ContractPage, PocketSchedule, PhoneNote, LotEvidence, Ledger, BellLetter, EvidenceChain,
  DivorceEnvelope, GarageMap, CaseWeb, DebtBeat, Countdown, ArrestTransition, ResusTimer, EvidenceRecap, AprilEpilogue,
};

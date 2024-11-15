from ReinventQC.reinvent_scoring.scoring.component_parameters import ComponentParameters
from ReinventQC.reinvent_scoring.scoring.score_components.physchem.base_physchem_component import BasePhysChemComponent
from rdkit import Chem
from rdkit.Chem import RDConfig
import os
import sys
sys.path.append(os.path.join(RDConfig.RDContribDir, 'SA_Score'))

class SAScore(BasePhysChemComponent):
    def __init__(self, parameters: ComponentParameters):
        import sascorer
        self.model = sascorer
        super().__init__(parameters)

    def _calculate_phys_chem_property(self, mol):
        sco = self.model.calculateScore(mol)

        return sco

from ReinventQC.reinvent_scoring.scoring.component_parameters import ComponentParameters
from ReinventQC.reinvent_scoring.scoring.score_components.physchem.base_physchem_component import BasePhysChemComponent
from rdkit import Chem
import os

class SCScore(BasePhysChemComponent):
    def __init__(self, parameters: ComponentParameters):
        from scscore.standalone_model_numpy import SCScorer, project_root

        super().__init__(parameters)
        model = SCScorer()
        self.scsmodel = model.restore(os.path.join(project_root, 'models', 'full_reaxys_model_1024bool', 'model.ckpt-10654.as_numpy.json.gz'))

    def _calculate_phys_chem_property(self, mol):
        smiles = Chem.MolToSmiles(mol)
        (smi, sco) = self.scsmodel.get_score_from_smi(smiles)

        return sco
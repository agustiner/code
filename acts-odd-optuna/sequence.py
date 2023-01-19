# in
# n_max_seeds_per_sp_m number of compatible 
# cot_theta_max cot of maximum theta angle
# sigmaScattering How many sigmas of scattering to include in seeds
# radLengthPerSeed Average Radiation Length. average radiation lengths of material on the length of a seed
# impactMax max impact parameter in mm
# maxPtScattering maximum Pt for scattering cut in GeV
# deltaRMin minimum value for deltaR separation in mm
# deltaRMax maximum value for deltaR separation in mm
# out
# .root file
# .root file
# .root file

import pathlib
import acts
import acts.examples
import acts.examples.simulation
from acts.examples.reconstruction import (
    addSeeding,
    TruthSeedRanges,
    ParticleSmearingSigmas,
    SeedfinderConfigArg,
    SeedingAlgorithm,
    TrackParamsEstimationConfig,
    CKFPerformanceConfig,
    addCKFTracks,
)    
from acts.examples.simulation import (
    MomentumConfig,
    EtaConfig,
    ParticleConfig,
    ParticleSelectorConfig,
)
from acts.examples.reconstruction import (
    TruthSeedRanges,
    CKFPerformanceConfig,
    VertexFinder,
    TrackSelectorRanges,
)
from acts.examples.simulation import (
    addParticleGun,
    EtaConfig,
    PhiConfig,
    ParticleConfig,
    addFatras,
    addDigitization,
)
from acts.examples import GenericDetector
import datetime
import os

def run(output_path,
        maxSeedsPerSpM,
        cotThetaMax,
        sigmaScattering,
        radLengthPerSeed,
        impactMax,
        maxPtScattering,
        deltaRMin,
        deltaRMax):
    # Run the Sequence, starting from instantiating events and ending
    # with reconstructed tracks. This sequence may be put into an
    # optimizer trial function.
    
    logger = acts.logging.getLogger("full_chain_odd")
    logger.info("Starting Sequence")
    truthSmearedSeeded = False
    truthEstimatedSeeded = False
    u = acts.UnitConstants
    
    detector, trackingGeometry, decorators = GenericDetector.create()
    field = acts.ConstantBField(acts.Vector3(0.0, 0.0, 2.0 * u.T))
    rnd = acts.examples.RandomNumbers(seed=42)

    acts_source_path = pathlib.Path('/home/user1/code/acts/source')
    digitization_file = acts_source_path / "Examples/Algorithms/Digitization/share/default-smearing-config-generic.json"
    geometry_selection_file = acts_source_path / "Examples/Algorithms/TrackFinding/share/geoSelection-genericDetector.json"
    
    s = acts.examples.Sequencer(events = 1,
                                outputDir = str(output_path))

    acts.examples.simulation.addParticleGun(
        s,
        EtaConfig(-2.0, 2.0),
        ParticleConfig(4, acts.PdgParticle.eMuon, True),
        PhiConfig(0.0, 360.0 * u.degree),
        multiplicity = 2,
        rnd = rnd,
    )
    
    acts.examples.simulation.addFatras(
        s,
        trackingGeometry,
        field,
        outputDirRoot = output_path,
        rnd = rnd,
    )
    
    acts.examples.simulation.addDigitization(
        s,
        trackingGeometry,
        field,
        digiConfigFile = digitization_file,
        outputDirRoot = output_path,
        rnd = rnd,
    )
    
    acts.examples.reconstruction.addSeeding(
        s,
        trackingGeometry,
        field,
        TruthSeedRanges(pt=(500 * u.MeV, None), nHits = (9, None)),
        ParticleSmearingSigmas(pRel=0.01),
        SeedfinderConfigArg(
            r=(None, 200 * u.mm),
            deltaR=(deltaRMin * u.mm, deltaRMax * u.mm),
            collisionRegion = (-250 * u.mm, 250 * u.mm),
            z=(-2000 * u.mm, 2000 * u.mm),
            maxSeedsPerSpM = maxSeedsPerSpM,
            cotThetaMax = cotThetaMax,
            sigmaScattering = sigmaScattering,
            radLengthPerSeed = radLengthPerSeed,
            maxPtScattering = maxPtScattering * u.GeV,
            minPt= 500 * u.MeV,
            bFieldInZ = 1.99724 * u.T,
            impactMax = impactMax * u.mm,
        ),
        TrackParamsEstimationConfig(deltaR=(10.0 * u.mm, None)),
        seedingAlgorithm=SeedingAlgorithm.TruthSmeared
        if truthSmearedSeeded
        else SeedingAlgorithm.TruthEstimated
        if truthEstimatedSeeded
        else SeedingAlgorithm.Default,
        geoSelectionConfigFile = geometry_selection_file,
        outputDirRoot = output_path,
        rnd = rnd,
    )

    acts.examples.reconstruction.addCKFTracks(
        s,
        trackingGeometry,
        field,
        CKFPerformanceConfig(ptMin = 400 * u.MeV, nMeasurementsMin = 6),
        outputDirRoot = output_path
    )
    
    s.run()

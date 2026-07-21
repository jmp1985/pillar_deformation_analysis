from pillar_deformation_analysis.main import analyse

if __name__ == "__main__":
    # The pixel size
    pixel_size = 1.93

    # The data directory
    data_dir = "/media/jmp/RFI/2025/Pillars/data"

    # The datasets
    datasets = [
        "PillarsExcellentAdventure/PillarsExcellentAdventure",
        "PillarsExcellentAdventure/PillarsBogusJourney",
        "NakedGunPillars/FromThePillarOfPoliceSquad",
        "NakedGunPillars/ThePillarInsult",
        "NakedGunPillars/ThePillarGun",
        "NakedGunPillars/TheSmellOfPillar",
        "AirplanePillars/AirPillar2TheSequel/Before_after_search",
        "IndianaJonesPillars/Pillars/KingdomOfTheCrystalPillar",
        "IndianaJonesPillars/Pillars/ThePillarOfDoom",
        "HerbiePillars/HerbiePillars/PillarGoesBananas",
        "HerbiePillars/HerbiePillars/ThePillarBug",
        "HerbiePillars/HerbiePillars/PillarGoesToMonteCarlo",
        "HerbiePillars/HerbiePillars/TheLovePillar",
        "HerbiePillars/HerbiePillars/PillarRidesAgain",
        "HerbiePillars/HerbiePillars/PillarFullyLoaded",
    ]

    # Do the pillar deformation analysis
    analyse(data_dir, datasets, pixel_size)

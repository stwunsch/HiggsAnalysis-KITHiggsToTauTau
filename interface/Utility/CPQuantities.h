
#pragma once

#include <utility>

#include "Kappa/DataFormats/interface/Kappa.h"
#include "Artus/Utility/interface/ArtusLogging.h"

#include "TVector3.h"


/**
   \brief Place to collect functions calculating CP quantities
   -Phi* : this is a variable, with which one can say, whether the considered boson is a CP even state or a CP odd state
   -Phi*CP : this is a variable, with which one can figure out, whether the Higgs is a CP mixture or not
   -Zs : this is a variable, with which one can figure out, wether the considered boson has spin 1 (Z) or 0 (Higgs)
*/

class CPQuantities
{
public:
	double CalculatePhiStarCP(RMFLV tau1, RMFLV tau2, RMFLV chargPart1, RMFLV chargPart2);
	double CalculatePhiStarCP(KVertex pv , KTrack track1, KTrack track2, RMFLV chargPart1,RMFLV chargPart2);
	double CalculatePhiStarCP_rho(RMFLV chargedPiP, RMFLV chargedPiM, RMFLV piZeroP, RMFLV piZeroM);
	double CalculatePhiStarCP(KRefitVertex* pv , KTrack track1, KTrack track2, RMFLV chargPart1, RMFLV chargPart2);
	double CalculateChargedHadronEnergy(RMFLV diTauMomentum, RMFLV chargHad);
	double CalculatePhiCP(RMFLV boson, RMFLV tau1, RMFLV tau2, RMFLV pion1, RMFLV pion2);
	double CalculateChargedProngEnergy(RMFLV tau, RMFLV chargedProng);
	double CalculateChargedProngEnergyApprox(RMFLV tau, RMFLV chargedProng);
	double CalculateSpinAnalysingDiscriminant_rho(RMFLV tau1, RMFLV tau2, RMFLV pionP, RMFLV pionM, RMFLV pi0P, RMFLV pi0M);
	double CalculateSpinAnalysingDiscriminant_rho(RMFLV pionP, RMFLV pionM, RMFLV pi0P, RMFLV pi0M);
	double CalculateTrackReferenceError(KTrack track);
	double CalculateZPlusMinus(RMFLV higgs, RMFLV chargedPart);
	double CalculateZs(double zPlus, double zMinus);
	double PhiTransform(double phi);
	TVector3 CalculateIPVector(KGenParticle* genParticle, RMPoint* pv);
	TVector3 CalculateIPVector(KLepton* recoParticle, KRefitVertex* pv);
	TVector3 CalculateIPVector(KLepton* recoParticle, KRefitVertex* pv, float lepDz);
	inline double GetGenPhiStar()
	{
		return genPhiStar;
	}
	inline double GetGenPhi()
	{
		return genPhi;
	}
	inline double GetRecoPhiStar()
	{
		return recoPhiStar;
	}
	inline double GetRecoIP1()
	{
		return recoIP1;
	}
	inline double GetRecoIP2()
	{
		return recoIP2;
	}
private:
	double genPhiStar;
	double genPhi;
	double recoPhiStar;
	double recoIP1;
	double recoIP2;
	//level: "gen", "reco"
	double CalculatePhiStarCPSame(RMFLV::BetaVector k1, RMFLV::BetaVector k2, RMFLV chargPart1, RMFLV chargPart2, std::string level);
	double CalculateOStarCPSame(RMFLV::BetaVector k1, RMFLV::BetaVector k2, RMFLV chargPart1, RMFLV chargPart2);
	inline void SetGenPhiStar(double genphistar)
	{
		genPhiStar = genphistar;
	}
	inline void SetGenPhi(double genphi)
	{
		genPhi = genphi;
	}
	inline void SetRecoPhiStar(double recophistar)
	{
		recoPhiStar = recophistar;
	}
	inline void SetRecoIP1(double recoip1)
	{
		recoIP1 = recoip1;
	}
	inline void SetRecoIP2(double recoip2)
	{
		recoIP2 = recoip2;
	}
};

import * as fs from "fs"

// Type definitions
export interface Offer {
  id: number
  title: string
  description: string
  category: number
  merchants: Array<Merchant>
  age_scores: AgeScore
  gender_scores: GenderScore
  valid_to: string
  total_score?: number
  merchant_min_dist?: Merchant
}

export interface Merchant {
  id: number
  name: string
  distance: number
}

export interface AgeScore {
  adults: number
  seniors: number
  young_adults: number
  teens: number
}

export interface GenderScore {
  male: number
  female: number
  non_binary: number
}

export interface OfferFormat {
  id: number
  title: string
  category: string
  description?: string
  valid_to?: string
}

type ageGroup = 'adults' | 'seniors' | 'young_adults' | 'teens'
type genderGroup = 'male' | 'female' | 'non_binary'

// Main class
export class OfferService {
  merchantOffers(checkin: string, offers: Array<Offer>, ageGroup: ageGroup, gender: genderGroup): Array<OfferFormat> {
    const filteredOffers = offers.filter((offer) => this.filterInvalidOffers(offer, checkin))

    filteredOffers.forEach((offer) => {
      const totalScore = offer.age_scores[ageGroup] * 1.25  + offer.gender_scores[gender] * 1.5
      offer.total_score = totalScore
      offer.merchant_min_dist = offer.merchants.reduce((min, current) => (current.distance < min.distance ? current : min), offer.merchants[0])
    })

    filteredOffers.sort(this.sortOffersByDistAndScore)

    const bestOffers = this.get2BestOffer(filteredOffers)

    return bestOffers
  }

  private filterInvalidOffers(offer: Offer, checkin: string): boolean {
    const checkinDate = new Date(checkin).getTime()
    const offerValidToDate = new Date(offer.valid_to).getTime()
    const oneDay = 24 * 60 * 60 * 1000; // hr * min * sec * ms
    const dayDifference = Math.floor((offerValidToDate - checkinDate) / oneDay)
  
    switch (offer.category) {
      case 1: {
        // Restaurant
        if (dayDifference > 3) {
          return true
        }
        break
      }
      case 2: {
        // Retail
        if (dayDifference > 5) {
          return true
        }
        break
      }
      case 4: {
        // Activity
        if (dayDifference > 7) {
          return true
        }
        break
      }
      default: {
        break
      }
    }
    return false
  }

  private sortOffersByDistAndScore(offer1: Offer, offer2: Offer): number {
    // Lower Distance priority, followed by highest score
    if (offer1.merchant_min_dist!.distance !== offer2.merchant_min_dist!.distance) {
      return offer1.merchant_min_dist!.distance - offer2.merchant_min_dist!.distance
    }
    return offer2.total_score! - offer1.total_score!
  }

  private get2BestOffer(offers: Array<Offer>): Array<OfferFormat> {
    let currentCategory = -1 // Since we only have 4, I assume -1 is assigned as none
    const bestOffers: Array<OfferFormat> = []

    for (var offer of offers) {
      const formattedOffer = this.formatOffer(offer)

      if (currentCategory == -1) {
        bestOffers.push(formattedOffer)
        currentCategory = offer.category
        continue
      } 
      if (currentCategory != offer.category) {
        bestOffers.push(formattedOffer)
        break
      }
    }
    return bestOffers
  }

  private formatOffer(offer: Offer): OfferFormat {
    switch (offer.category) {
      case 1: {
        return {
          id: offer.id,
          title: offer.title,
          description: offer.description,
          category: "Restaurant"
        }
      }
      case 2: {
        return {
          id: offer.id,
          title: offer.title,
          category: "Retail"
        }
      }
      case 4: {
        return {
          id: offer.id,
          title: offer.title,
          description: offer.description,
          valid_to: offer.valid_to,
          category: "Activity"
        }
      }
      default: {
        break
      }
    }
    throw new Error('Unexpected category type, expected 1, 2 or 4 only')
  }

}

const rawData = fs.readFileSync("offers.json", "utf8")
const jsonData: Array<Offer> = JSON.parse(rawData)
const offerService = new OfferService()

// offerService.merchantOffers('2023-05-15', jsonData, 'young_adults', 'male')
// offerService.merchantOffers('2023-05-15', jsonData, 'teens', 'male')
// offerService.merchantOffers('2023-05-15', jsonData, 'seniors', 'female')
console.log(offerService.merchantOffers('2023-05-15', jsonData, 'young_adults', 'male'))

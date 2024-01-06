interface PredictionData {
  linPred: number;
  nnwPred: number;
  nntPred: number;
  totalSent: number[];
  weightedSent: number[];
  numReviews: number;
  sentMatrix: number[][];
  sentences: string[];
}

const sampleSentMatrix = [
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
  [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
  [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
];

const sampleText = `Visiting Davis for the first time over parents weekend and sropped here for a quick meal. This is a place that clearly caters to students who want the most mass for the dollar and that is the lone fact that describes the appeal of eating here.
\npork, beef, chicken plates ordered. meat seasoning is too salty and chicken is too burnt. It's not good for health. I don't like that. No good.
\nTim's Hawaiian is a pretty good to go spot that I enjoy coming to when I want my greens carbs and protein. There is limited seating inside but plenty of room with shade outside! Service could be a little faster but the staff is friendly.
\nNice food with fairly quick service. Good outdoor seating and limited indoor seating, but popularity is greater than seating capacity. Very meat forward dishes, with heavy helpings of white rice. The bowls have a better mix of vegetables, but still very lopsided nutritionally.
\nI'm fairly new to Davis and thought I'd try something new . I ordered the chicken Katsu plate with rice and macaroni salad and I got severe food poisoning and had to be hospitalized the last two days . I thought it would be good because of all the great reviews but maybe they were just having an off day. I'm very disappointed and still very sick .
\nFirst impressions: plenty of outdoor seating with shaded areas from the afternoon sun. The inside has fewer seats but is homely with brightly colored decor. Friendly and welcoming staff define the experience. I ordered the highly recommended katsu rice bowl to-go, which maintained its crispiness even after my trip home. I would suggest adding the sauce to the bowl, as the vegetables are rather bland. Overall, a solid, filling choice. I'll be back to try their BBQ!
\nGreat job Tim's! Kalbi beef ribs were incredible! Girl at the counter was helpful too...
\nSeating is a little cozy, AC didn't seem to work well, and we had to use those orange ordering kiosks that seem to add on random fees and then ask for a tip but the food portions were generous and it was very delicious. We should have split plates between people, it was so filling.
\nGood food and my order was ready quickly. It's a good price for the amount of food you get (I got bbq mix). They seem to order with services like door dash etc. During covid inside dining not happening but they have a nice outside patio you can eat on. Hand sanitizer available and their menu is online.
\nThe short ribs and macaroni salad were good. The barbecued pork was amazing. I wanted to keep taking it from my wife's plate.
\nHands down some really good food! I ordered the bbq mix plate, not only was I filled but satisfied. The meat is tender, juicy and had a perfect amount of sides. Such as white rice (two scoops), cabbage, ande some macaroni salad. The plate was about $13, to me it's a reasonable     price for all food I received so when you get a chance I would try this place.
\nGreat place and locale. Right off of campus in a little yellow building. Prices good, servings could be bigger. My friend got the loco moco(with the fried egg) and I got the chicken katsu
\nHuge portions. Got the BBQ mix plate and it's honestly enough for two meals. Recommend the BBQ beef and chicken. The short ribs were a little too tough. The Mac salad is really good here.
\nThe Loco moco is so got damn good omg that so season my egg was cooked rite the beef patty was on point the gravy was heavenly good lmao all I can say is Gaaaaawd damn`;

const sampleSentences = [
  "Visiting Davis for the first time over parents weekend and sropped here for a quick meal.",
  "This is a place that clearly caters to students who want the most mass for the dollar and that is the lone fact that describes the appeal of eating here.",
  "pork, beef, chicken plates ordered.",
  "meat seasoning is too salty and chicken is too burnt.",
  "It's not good for health.",
  "I don't like that.",
  "No good.",
  "Tim's Hawaiian is a pretty good to go spot that I enjoy coming to when I want my greens carbs and protein.",
  "There is limited seating inside but plenty of room with shade outside!",
  "Service could be a little faster but the staff is friendly.",
  "Nice food with fairly quick service.",
  "Good outdoor seating and limited indoor seating, but popularity is greater than seating capacity.",
  "Very meat forward dishes, with heavy helpings of white rice.",
  "The bowls have a better mix of vegetables, but still very lopsided nutritionally.",
  "I'm fairly new to Davis and thought I'd try something new .",
  "I ordered the chicken Katsu plate with rice and macaroni salad and I got severe food poisoning and had to be hospitalized the last two days .",
  "I thought it would be good because of all the great reviews but maybe they were just having an off day.",
  "I'm very disappointed and still very sick .",
  "First impressions: plenty of outdoor seating with shaded areas from the afternoon sun.",
  "The inside has fewer seats but is homely with brightly colored decor.",
  "Friendly and welcoming staff define the experience.",
  "I ordered the highly recommended katsu rice bowl to-go, which maintained its crispiness even after my trip home.",
  "I would suggest adding the sauce to the bowl, as the vegetables are rather bland.",
  "Overall, a solid, filling choice.",
  "I'll be back to try their BBQ!",
  "Great job Tim's!",
  "Kalbi beef ribs were incredible!",
  "Girl at the counter was helpful too...",
  "Seating is a little cozy, AC didn't seem to work well, and we had to use those orange ordering kiosks that seem to add on random fees and then ask for a tip but the food portions were generous and it was very delicious.",
  "We should have split plates between people, it was so filling.",
  "Good food and my order was ready quickly.",
  "It's a good price for the amount of food you get (I got bbq mix).",
  "They seem to order with services like door dash etc.",
  "During covid inside dining not happening but they have a nice outside patio you can eat on.",
  "Hand sanitizer available and their menu is online.",
  "The short ribs and macaroni salad were good.",
  "The barbecued pork was amazing.",
  "I wanted to keep taking it from my wife's plate.",
  "Hands down some really good food!",
  "I ordered the bbq mix plate, not only was I filled but satisfied.",
  "The meat is tender, juicy and had a perfect amount of sides.",
  "Such as white rice (two scoops), cabbage, ande some macaroni salad.",
  "The plate was about $13, to me it's a reasonable     price for all food I received so when you get a chance I would try this place.",
  "Great place and locale.",
  "Right off of campus in a little yellow building.",
  "Prices good, servings could be bigger.",
  "My friend got the loco moco(with the fried egg) and I got the chicken katsu",
  "Huge portions.",
  "Got the BBQ mix plate and it's honestly enough for two meals.",
  "Recommend the BBQ beef and chicken.",
  "The short ribs were a little too tough.",
  "The Mac salad is really good here.",
  "The Loco moco is so got damn good omg that so season my egg was cooked rite the beef patty was on point the gravy was heavenly good lmao all I can say is Gaaaaawd",
  "damn",
];

export { sampleSentMatrix, sampleText, sampleSentences };
export type { PredictionData };

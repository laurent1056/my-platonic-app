export interface FounderStory {
  title: string
  intro: string
  sections: [string, string][]
  homepageSections: [string, string][]
}

export const founderStory: FounderStory = {
  title: 'Why I built Platonic Ideal.',
  intro: 'I wanted to bring a search for first principles into an ordinary act: deciding what is worth owning.',
  sections: [
    ['A return to first principles.', 'I am Laurent Courtines. I am Catholic, and my faith was the beginning of a philosophical journey. As the world felt increasingly loud, hurried, and difficult to interpret—with politics, cultural conflict, and the general speed of modern life—I wanted to return to more fundamental questions: what things are, what they are for, and what standards should govern our judgment.'],
    ['From Forms to products.', 'I began reading and listening to people discuss Plato, Aristotle, and the history of philosophy. Plato’s theory of Forms especially stayed with me: the idea that things are not only individual material objects, but participate in recognizable ideals. There is such a thing as a cat—not only this cat or that cat, but the form of what a cat is. Our minds can recognize that form even when every individual example is imperfect.'],
    ['The consumer problem.', 'That made me wonder whether the same idea could apply to the things we buy. We built the internet, search engines, review sites, comparison tools, and influencer channels to help us decide what is good. Yet the result is often more noise. Affiliate marketing, popularity, and constant content production make it difficult to know what to trust. When the choices become overwhelming, people often default to the most familiar brand simply because the decision carries too much cognitive load.'],
    ['A standard for the thing.', 'I wanted a place with explicit rules and a clear standard. When I say raincoat, I want to know what a raincoat should be: durable, useful, dependable, and capable of surviving real ownership. Platonic Ideal examines construction, maintenance, failure, repairability, permanence, and evidence. When a product meets the standard, we name it. When none does, we keep the answer open.'],
    ['The refrigerator test.', 'The refrigerator entry in the register is a useful example of an honest no. Its current analysis identifies sealed compressor systems with proprietary refrigerants, electronic control boards that can fail unpredictably, and repair economics in which a $150–200 diagnostic visit plus parts can approach or exceed replacement cost. A qualifying refrigerator would need mechanical controls, a compressor replaceable for less than 40% of a new unit, long parts availability, and published repair manuals. The empty verdict is not a failure to research; it is the result of applying the standard.'],
    ['A project I wanted to build.', 'I also wanted to practice my AI building skills. Platonic Ideal became a fascinating way to marry two interests: learning about Plato and philosophy, then applying first principles to a practical question in e-commerce and buying. Building the product, the register, the editorial rules, and the experience gave me a way to turn that philosophical interest into something people could use.'],
    ['An authority you can inspect.', 'The goal is not to remove judgment from people’s lives. It is to spare them from repeating endless product research every time they need something. The verdict is not an affiliate placement or a paid ranking. The public judgment should remain free and independent; the dossier can sell research depth and convenience, never influence. Authority here has to be earned through transparent rules, evidence, and the willingness to say that no product qualifies.'],
  ],
  homepageSections: [
    ['A return to first principles.', 'I am Catholic, and my faith began a philosophical journey that brought me back to Plato, Aristotle, and the question of what things really are in a world full of noise, politics, cultural conflict, and competing incentives.'],
    ['From Forms to products.', 'Plato’s Forms made me wonder whether everyday products could also be judged against an ideal: not the most popular object, but the one that best realizes what the category is for.'],
    ['Reduce the cognitive load.', 'We have built an enormous review economy to help us choose, yet more information often leaves us less certain. Platonic Ideal does the comparison work once, using explicit rules about construction, maintenance, failure, repairability, permanence, and evidence.'],
    ['One product. Or an honest no.', 'The refrigerator entry stays empty because its current analysis finds sealed compressor systems, unpredictable control-board failures, and repair economics that can approach replacement cost. A clear empty verdict is more useful than forcing a recommendation that has not earned its place.'],
    ['Why build it?', 'I wanted to practice my AI building skills while bringing philosophy into a practical e-commerce question. The result is a place where the public verdict stays free, the reasoning stays inspectable, and any future dossier can support depth without buying influence.'],
  ],
}

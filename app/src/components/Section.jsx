import React from "react";

function Section({ heading, cards }) {
  return (
    <section className="text-center py-5">
      <h2>{heading}</h2>
      <div className="row justify-content-center mt-4 ">
        {cards.map((card, index) => (
          <div key={index} className="col-md-4">
            <div className="feature-card p-3 bg-light rounded py-5">
              <h3>{card.title}</h3>
              {card.icon && <div className="mb-2">{card.icon}</div>}
              <p>{card.description}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

export default Section;

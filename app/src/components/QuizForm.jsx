import React from "react";

function QuizForm({ question, options, questionIndex }) {
  return (
    <div className="quiz-container p-4 border rounded bg-light">
      <h5 className="mb-3">{question}</h5>
      <form>
        {options.map((option, i) => (
          <div key={i} className="form-check">
            <input
              className="form-check-input"
              type="radio"
              name={`question-${questionIndex}`}
              id={`question-${questionIndex}-option-${i}`}
            />
            <label
              className="form-check-label"
              htmlFor={`question-${questionIndex}-option-${i}`}
            >
              {option}
            </label>
          </div>
        ))}
      </form>
    </div>
  );
}

export default QuizForm;

const dateFormatter = new Intl.DateTimeFormat("en-US", {
  year: "numeric",
  month: "long",
  day: "numeric",
  hour: "2-digit",
  minute: "numeric",
});

const shortDateFormatter = new Intl.DateTimeFormat("en-US", {
  year: "numeric",
  month: "long",
  day: "numeric",
});

const veryShortDateFormatter = new Intl.DateTimeFormat("es-CO", {
  year: "numeric",
  month: "numeric",
  day: "numeric",
});

const hourFormatter = new Intl.DateTimeFormat("es-CO", {
  hour: "2-digit",
  minute: "numeric",
  second: "numeric",
});

const shortHourFormatter = new Intl.DateTimeFormat("es-CO", {
  hour: "2-digit",
  minute: "numeric",
  second: "numeric",
});

export const parseStringToShortDate = (dateAsString) => {
  if (!dateAsString) {
    return "-";
  }
  const date = new Date(dateAsString);
  return shortDateFormatter.format(date);
};

export const parseStringToVeryShortDate = (dateAsString) => {
  if (!dateAsString) {
    return "-";
  }
  const date = new Date(dateAsString);
  return veryShortDateFormatter.format(date);
};

export const parseStringToDetailedDate = (dateAsString) => {
  if (!dateAsString) {
    return "-";
  }
  const date = new Date(dateAsString);

  return dateFormatter.format(date);
};

export const dateToShortString = (date) => {
  return shortDateFormatter.format(date);
};

export const dateToLongString = (date) => {
  return dateFormatter.format(date);
};

export const getHourAndMinutes = (date) => {
  return shortHourFormatter.format(date);
};

export const getTimeInString = () => {
  return hourFormatter.format(Date.now());
};

export const getCurrentYear = () => {
  return new Date().getFullYear();
};

export const isSameDate = (dateOne, dateTwo) => {
  return (
    dateOne.getFullYear() === dateTwo.getFullYear() &&
    dateOne.getMonth() === dateTwo.getMonth() &&
    dateOne.getDate() === dateTwo.getDate()
  );
};

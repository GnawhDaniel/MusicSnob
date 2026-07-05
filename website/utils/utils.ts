const months = [
  "Jan",
  "Feb",
  "Mar",
  "Apr",
  "May",
  "Jun",
  "Jul",
  "Aug",
  "Sep",
  "Oct",
  "Nov",
  "Dec",
];

export function formatDate(date: string) {
  // Expects YYYY-MM-DD
  let res = new Date(date);
  return `${months[res.getMonth()]} ${res.getDate()}, ${res.getFullYear()}`
}

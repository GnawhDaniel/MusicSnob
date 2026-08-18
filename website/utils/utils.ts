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
  const res = new Date(date);
  return `${months[res.getUTCMonth()]} ${res.getUTCDate()}, ${res.getUTCFullYear()}`;
}

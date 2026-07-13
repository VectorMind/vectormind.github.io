const args = process.argv.slice(2);
const value = (name) => {
  const index = args.indexOf(name);
  return index >= 0 ? args[index + 1] : null;
};

console.log(JSON.stringify({
  context: "org.harborworks.domain.customer.operations",
  revision: "customer-r1",
  skill: value("--skill"),
  knowledge: value("--knowledge"),
  message: "hello from the Harborworks Node fixture"
}));

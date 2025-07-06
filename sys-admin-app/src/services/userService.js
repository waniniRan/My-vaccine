const getAllUsers = async () => {
  const res = await fetch("/api/users/", {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
      "Content-Type": "application/json",
    },
  });

  if (!res.ok) {
    // optionally you can parse the error if your Django sends JSON errors
    let errorText = "Failed to fetch users";
    try {
      const errorData = await res.json();
      if (errorData.detail) errorText = errorData.detail;
    } catch (e) {
      // swallow JSON parse errors
    }
    throw new Error(errorText);
  }

  return res.json();
};

export default {
  getAllUsers,
};

const tokenName: string = "workNumberToken";

export const getToken = () => {
    return localStorage.getItem(tokenName);
}

const setToken = (token: string) => {
    localStorage.setItem(tokenName, token)
}
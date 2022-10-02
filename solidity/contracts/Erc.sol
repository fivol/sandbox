
pragma solidity ^0.8.0;

contract ERC20 is IERC20 {
	uint totalTokens;
	
	constoructor(string memory name_, string memory symbol_, uint initialSupply, address shop) {
		_name = name_;
		_symbol = symbol_;
		owner = msg.sender;
		mint(initialSupply, shop);
	}
	
	funciton mint(uing amount, address shop) public onlyOwner {
		balance[shop] += amount;
		totalTokens += amount;
		emit Transfer(address(0), shop, amount);
	}
	
	function decimals() external pure returns(uint) {
		return 18;
	}
	function totalSupply() external {
		return totalTokens
	}
	function balanceOf(address account) public view returns(uint) {
		return balances[account];
	}
	
	function mint(uint amount, address shop) {
		
	}
	
	function transfer(address to, uint amount) external {
		balances[msg.sender] -= amount;
		balances[to] += amount;
		emit Transfer(msg.sender, to, amount);
	}
	
	function _beforeTokenTransfer(address from, address to, uint amount) internal virtual {
		
	}
	
	function allownce(address _owner, address spender) {
	}

    function transferFrom(address sender, address recipient, uint amount) public {
        _beforeTokenTransfer(sender, recipient, amount);
        allownces[sender][recipient] -= amount;

        balances[sender] -= amount;
        balances[recipient] += amount;
        emit Transfer(sender, recipient, amount);
    }
}

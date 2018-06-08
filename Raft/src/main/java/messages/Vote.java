package messages;

import java.io.Serializable;

import info.HostInfo;
import ledger.Ledger;
import ledger.Log;
import routing.Route;

/**
 * This class is designed to be serialized and sent across a network. Therefore, it implements Serializable.
 * 
 * The Vote Object will be instantiated and sent to all Nodes available in a Candidate's Routing Table. 
 * The rpc will then modify the Vote Object, to signify that a vote has been cast for a candidate.
 * 
 * @author deenaariff
 *
 */
public class Vote implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private boolean isVoteCast;
	private String ip;
	private int voting_port;
	private int endpoint_port;
    private Route route;
    private int term;
    private int responder;
    private int last_log_index;
    private int last_log_term;
	
	/**
	 * The Constructor for the Vote Class.
	 * 
	 * @param host The host of the origin that is requesting the Vote.
	 */
	public Vote(HostInfo host, Ledger ledger) {
		this.isVoteCast = false;
		this.ip = host.getHostName();
		this.voting_port = host.getVotingPort();
		this.endpoint_port = host.getEndPointPort();
		this.route = host.getRoute();
		this.term = host.getTerm();
		Log last_log = ledger.getLastLog();

		if(last_log == null) {
			this.last_log_index = 0;
			this.last_log_term = host.getTerm();
		} else {
			this.last_log_index = last_log.getIndex();
			this.last_log_term = last_log.getTerm();
		}
	}

    public Route getRoute() {
        return route;
    }

    /**
	 * The method a rpc uses to cast a vote for a Candidate.
	 */
	public void castVote(int id) {
		this.isVoteCast = true;
		this.responder = id;
	}

	public int getLastLogIndex() { return this.last_log_index; }

	public int getLastLogTerm() { return this.last_log_term; }

	public int getResponder() {
		return this.responder;
	}

	
	/**
	 * This return's the vote status of the Vote Object
	 */
	public boolean getVoteStatus () {
		return this.isVoteCast;
	}

	public int getEndpointPort() { return this.endpoint_port; };
	
	/**
	 * This returns the vote's origin host
	 */
	public String getHostName() {
		return this.ip;
	}

	/**
	 * This return's the vote's origin hosts' port that is being listened on
	 */
	public int getVotingPort() {
		return this.voting_port;
	}

    /**
     * This returns the vote's origin host's term
     */
    public int getTerm() { return this.term; }

}

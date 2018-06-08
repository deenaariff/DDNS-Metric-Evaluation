package node;
import rpc.rpc;
import info.HostInfo;
import ledger.Ledger;
import routing.RoutingTable;
import voting_booth.VotingBooth;

import java.util.concurrent.TimeUnit;

/**
 * This is the class that contains the implementation of the Weave Node and
 * for switching between states. This class passes essential information to 
 * each class that implements various state_helpers's logic.
 * 
 * @author deenaariff
 */
public class RaftNode implements Runnable {
	
	private Ledger ledger;
	private HostInfo host;
	private RoutingTable rt;
	private VotingBooth vb;

	/**
	 * Constructor for the RaftNode Class.vb
     * Pass option Routing Table
	 *
	 */
	public RaftNode(RoutingTable rt, Ledger ledger, HostInfo host, VotingBooth vb) {
        this.rt = rt;
        this.host = host;
        this.ledger = ledger;
        this.vb = vb;
    }

	public void run() {

        try{
            TimeUnit.SECONDS.sleep(1);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        while(!Thread.currentThread().isInterrupted()) {
            synchronized (this) {
                if(this.host.isLeader()) {
                    this.host.getLogger().log("Last Index Committed: " + this.ledger.getCommitIndex());
                    this.host.getLogger().log("Logs in Ledger: " + this.ledger.getLastApplied());
                    this.host.getLogger().log("Broadcasting Messages to Followers ");
                    try {
                        Thread.sleep(this.host.getHeartbeatInterval());
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                        break;
                    }
                    rpc.broadcastHeartbeatUpdates(this.rt, this.ledger, this.host);
                }
            }
        }

    }
	
}
